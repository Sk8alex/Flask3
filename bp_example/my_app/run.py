import os, sys
sys.path.append(os.path.pardir)
from my_app import create_app
from my_app.config import ProductionConfig


app = create_app()
# # print(app.config)  #конфигурация по умолчанию
# app.config.from_object("my_app.config.DevelopmentConfig")

# print("\n === After loading config === \n")
# print(app.config) #Словарь настроек для запуска приложения flask

if __name__ == '__main__':
    app.run(
        port=ProductionConfig.PORT, 
        host=ProductionConfig.SERVER_NAME, 
        debug=ProductionConfig.DEBUG
        )