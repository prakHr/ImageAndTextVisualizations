#!/usr/bin/env python
# coding: utf-8

# In[1]:


from docarray import Document, DocumentArray
from jina import Executor, Flow, requests


# In[2]:


class PreprocImg(Executor):
    @requests
    async def foo(self, docs: DocumentArray, **kwargs):
        for d in docs:
            (
                d.load_uri_to_image_tensor()  # load
                .set_image_tensor_normalization()  # normalize color
                .set_image_tensor_channel_axis(
                    -1, 0
                )  # switch color axis for the PyTorch model later
            )
            
class EmbedImg(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        import torchvision
        self.model = torchvision.models.resnet50(pretrained=True)        

    @requests
    async def foo(self, docs: DocumentArray, **kwargs):
        docs.embed(self.model)
        
class MatchImg(Executor):
    _da = DocumentArray()

    @requests(on='/index')
    async def index(self, docs: DocumentArray, **kwargs):
        self._da.extend(docs)
        docs.clear()  # clear content to save bandwidth

    @requests(on='/search')
    async def foo(self, docs: DocumentArray, **kwargs):
        docs.match(self._da, limit=9)
        del docs[...][:, ('embedding', 'tensor')]  # save bandwidth as it is not needed




# In[ ]:


from jina import Client

if __name__ == '__main__':
    # In[3]:


    f = (
        Flow(port=12345)
        .add(uses=PreprocImg)
        .add(uses=EmbedImg, replicas=3)
        .add(uses=MatchImg)
    )

    f.protocol='http'
    # In[4]:


    all_images_path = 'C:/Users/gprak/Downloads/Indian_Thai_BankNotes_Dataset/Indian_Thai_BankNotes_Dataset/**/**/**/*.jpg'

    index_data = DocumentArray.from_files(all_images_path,sampling_rate=0.01)


    # In[ ]:


    with f:
        f.post(
            '/index',
            index_data,
            show_progress=True,
            request_size=16,
        )
        f.block()

    c = Client(port=12345)  # connect to localhost:12345
    #print(c.post('/search', index_data[0])['@m'])  # '@m' is the matches-selector

