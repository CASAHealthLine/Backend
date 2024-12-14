import subprocess
import os

if __name__ == "__main__":
    venv_activate = os.path.join('.venv', 'Scripts', 'activate')
    
    # Chạy Django server trong môi trường ảo
    django_process = subprocess.Popen(f"{venv_activate} && python manage.py runserver", shell=True)
    
    # Chạy module Python khác
    module_process = subprocess.Popen(f"{venv_activate} && python -m telegram_bot.bot", shell=True)
    
    django_process.wait()
    module_process.wait()
