import subprocess

result = subprocess.run(["echo", "Привет из терминала"], capture_output=True, text=True, encoding='utf-8')

print(result.stdout) 