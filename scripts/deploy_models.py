from xinference.client import RESTfulClient
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def deploy_all_models():
    client = RESTfulClient("http://127.0.0.1:9997")
    
    try:
        # 先检查已部署的模型
        deployed_models = client.list_models()
        deployed_names = [m.model_name for m in deployed_models]
        logger.info(f"Already deployed models: {deployed_names}")
        
        # 获取可用模型列表
        registrations = client.list_model_registrations(model_type="LLM")
        
        # 只部署未部署的内置聊天模型
        models_to_deploy = []
        for reg in registrations:
            if isinstance(reg, dict):
                model_name = reg.get('model_name')
                is_builtin = reg.get('is_builtin', False)
                if (model_name and is_builtin and 
                    'chat' in model_name.lower() and 
                    model_name not in deployed_names):
                    models_to_deploy.append((model_name, "LLM"))
        logger.info("Available LLM models:")
        for reg in registrations:
            logger.info(f"Model: {reg}")
            
        # 只部署包含 chat 的模型
        models_to_deploy = []
        for reg in registrations:
            if isinstance(reg, dict):
                logger.info(f"reg info:{reg}")
                model_name = reg.get('model_name')
                if model_name and 'chat' in model_name.lower():  # 筛选包含 chat 的模型
                    models_to_deploy.append((model_name, "LLM"))
        
        logger.info(f"Chat models to deploy: {models_to_deploy}")
    
        for model_name, model_type in models_to_deploy:
            try:
                logger.info(f"Deploying {model_name}...")
                result = client.launch_model(
                    model_name=model_name,  # 换用 ChatGLM2-6B 模型
                    model_type=model_type,
                    model_engine="Transformers",
                    model_format="pytorch",
                    model_size="6",
                    quantization="8-bit",
                    device="cpu",
                    trust_remote_code=True,
                    use_safetensors=True,
                    model_kwargs={
                        "low_cpu_mem_usage": True
                    }
                )
                print(f"Result: {result}, Type: {type(result)}, Length: {len(result) if hasattr(result, '__len__') else 'N/A'}")
                a, b = result  # 这里会出错如果result包含超过2个元素
                logger.info(f"Successfully deployed {model_name}, uid: {b}")
                time.sleep(2)
            except Exception as e:
                logger.error(f"Failed to deploy {model_name}: {str(e)}")
    except Exception as e:
        logger.error(f"Error during model deployment: {str(e)}")

if __name__ == "__main__":
    deploy_all_models()