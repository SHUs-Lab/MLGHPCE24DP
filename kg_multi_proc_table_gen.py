import subprocess
ind = 0
i = 3000
processes = []
while i < 4000:
    p = subprocess.Popen(["python", "kg_gen_script.py", f"{i}", f"{i+99}" , f"{ind}"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(p.pid)
    processes.append(p)
    i += 100
    ind += 1
print("Processes queued")
for process in processes:
    process.wait()
print("Finished all processes")

ind = 0
i = 3000
processes = []
while i < 4000:
    p = subprocess.Popen(["python", "kg_gen_script.py", f"{i}", f"{i+99}" , f"{ind}", "-n"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(p.pid)
    processes.append(p)
    i += 100
    ind += 1
print("Processes queued")
for process in processes:
    process.wait()
print("Finished all processes")