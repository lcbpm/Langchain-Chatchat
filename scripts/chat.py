from xinference.client import Client

# 首先获取已部署模型的 UID
client = Client("http://localhost:9997")
models = client.list_models()
if not models:
    raise RuntimeError("没有找到已部署的模型，请先运行 deploy_models.py 部署模型")

# 使用第一个可用的模型
model = client.get_model(models[0].model_uid)

# Chat to LLM
model.chat(
   messages=[{"role": "system", "content": "You are a helpful assistant"}, {"role": "user", "content": "What is the largest animal?"}],
   generate_config={"max_tokens": 1024}
)

# Chat to VL model
model.chat(
   messages=[
     {
        "role": "user",
        "content": [
           {"type": "text", "text": "What’s in this image?"},
           {
              "type": "image_url",
              "image_url": {
                 "url": "http://i.epochtimes.com/assets/uploads/2020/07/shutterstock_675595789-600x400.jpg",
              },
           },
        ],
     }
  ],
  generate_config={"max_tokens": 1024}
)