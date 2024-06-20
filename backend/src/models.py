from transformers import CLIPProcessor, CLIPModel

class CLIPModelSingleton:
    _model = None
    _processor = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        return cls._model

    @classmethod
    def get_processor(cls):
        if cls._processor is None:
            cls._processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        return cls._processor
