
import argparse
import cmd
import os
import shlex
import docker
import tabulate
import numpy as np


class CM(cmd.Cmd):
    intro = ""
    prompt = "Cluster Manager>>> "
    ct_number = 0
    ct_list = []
    filepath=".\\CMDATA.txt"
    client = docker.from_env()
##command='bash',detach=True,stdin_open=True,tty=True,stdout=True
##client = docker.from_env()
##
    def __init__(self):
        super().__init__(self)
        self.intro = ""
        self.prompt = "Cluster Manager>>> "
        self.ct_number = 0
        self.ct_list = []
        self.filepath=".\\CMDATA.txt"
        self.client =  docker.from_env()   
##
    def preloop(self):
        print("/-----------------------------------------/\n\tWelcome to Cluster Manager\n/-----------------------------------------/")
        CM.do_list_container(self,line=None)
        print("/---------------------------------------------/\n\tEnter quit to quit\n/---------------------------------------------/")
        return super().preloop()
####
    def do_readfile(self):
        CM.ct_list=[]   
        ##   reset before reloading the container list data
        CM.ct_number=0
        ##  reset before reloading the container number data
        try:
            file = open(CM.filepath, "r")
            for row in file.readlines():
                row = row.strip()
                row = row.strip(",")
                row = row.strip("\n")
                row = row.split(",")
                CM.ct_list.append(row)
            file.close()
            CM.ct_number = len(CM.ct_list)        
        except FileNotFoundError:
            print("FileNotFound!")
            return []
        except IOError:
            print("IOError relating file occured!")
            return []
####    
    def do_writefile(self):
        try:
            file = open(CM.filepath, "w")
            for containers in CM.ct_list:
                for status in containers:
                    file.write(status+",")
                file.write("\n")
            CM.ct_number=len(CM.ct_list)
            file.close()   
        except FileNotFoundError:
            print("FileNotFound!")
            return []
        except IOError:
            print("IOError relating file occured!")
            return []   
#### 
    def do_refresh(self):
        try:
            list = CM.client.containers.list(all)
            CM.ct_list = []
            CM.ct_number = 0
            CM.ct_number = len(list)
            for i in range(CM.ct_number):
                temp = CM.ct_number-1-i
                CM.ct_list.append([str(list[temp].name),str(list[temp].short_id),str(list[temp].image),str(list[temp].status)])

        except docker.errors.APIError as e:
            print("an error occured when listing containers:", e) 
####    even better if sorting codes can be added
####
    def do_list_container(self,line):
        CM.do_refresh(self)
        CM.do_writefile(self)
        print("/-----------------------------------------/\n\tContainers Status List")
        print(f"\t{CM.ct_number} containers in total\n")
        table = tabulate.tabulate(CM.ct_list, headers=["Container Name", "Container ID", "Container Image", "Container Status"])
        print(table)
        print("/-----------------------------------------/")                
####
    def do_delete_container(self, line):
        CM.do_refresh(self)
        CM.do_writefile(self)    
        parser = argparse.ArgumentParser()
        parser.add_argument('-number', help='Specify the number')
        parser.add_argument('-name', help='Specify a name')
        args = parser.parse_args(shlex.split(line))

        if(args.name and args.number):
                print(f'please enter either a name or a number')
        elif((args.name is None) and (args.number is None)):
                print(f'please enter either a name or a number')
        elif(args.name and (args.number is None)):
                container_name = args.name
                try:
                    delete_container = CM.client.containers.get(container_name)
                    delete_container.stop()
                    delete_container.remove()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                except docker.errors.NotFound as e:
                    print("container not found when deleting containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when deleting containers:\n", e)                
        elif((args.name is None) and args.number):      
            if(args.number):
                temp = int(args.number)
            else:
                    temp = 1
            i=0
            while i < temp:
                container_name = CM.ct_list[CM.ct_number-1][0]
                ##  the delete process starts from th end of the container list
                ##  the create process starts from the head of the container list
                try:
                    delete_container = CM.client.containers.get(container_name)
                    delete_container.stop()
                    delete_container.remove()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                    i = i + 1
                except docker.errors.NotFound as e:
                    print("container not found when deleting containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when deleting containers:\n", e)
        CM.do_list_container(self,line=None) 
##
    def do_stop_container(self,line):
        CM.do_refresh(self)
        CM.do_writefile(self)     
        parser = argparse.ArgumentParser()
        parser.add_argument('-number', help='Specify the number')
        parser.add_argument('-name', help='Specify a name')
        args = parser.parse_args(shlex.split(line))

        if(args.name and args.number):
                print(f'please enter either a name or a number')
        elif((args.name is None) and (args.number is None)):
                print(f'please enter either a name or a number')
        elif(args.name and (args.number is None)):
                container_name = args.name
                try:
                    delete_container = CM.client.containers.get(container_name)
                    delete_container.stop()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                except docker.errors.NotFound as e:
                    print("container not found when stopping containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when stopping containers:\n", e)                
        elif((args.name is None) and args.number):      
            if(args.number):
                    temp = int(args.number)
            else:
                    temp = 1
            i=0
            while i < temp:
                container_name = CM.ct_list[CM.ct_number-1-i][0]
                ##  the stop process starts from the end of the container list
                ##  the start process starts from the end of the container list
                try:
                    delete_container = CM.client.containers.get(container_name)
                    delete_container.stop()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                    i = i + 1
                except docker.errors.NotFound as e:
                    print("container not found when stopping containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when stopping containers:\n", e)
        CM.do_list_container(self,line=None) 
##
    def do_start_container(self,line):
        CM.do_refresh(self)
        CM.do_writefile(self)  
        parser = argparse.ArgumentParser()
        parser.add_argument('-number', help='Specify the number')
        parser.add_argument('-name', help='Specify a name')
        args = parser.parse_args(shlex.split(line))

        if(args.name and args.number):
                print(f'please enter either a name or a number')
        elif((args.name is None) and (args.number is None)):
                print(f'please enter either a name or a number')
        elif(args.name and (args.number is None)):
                container_name = args.name
                try:
                    start_container = CM.client.containers.get(container_name)
                    start_container.start()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                except docker.errors.NotFound as e:
                    print("container not found when starting containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when starting containers:\n", e)                
        elif((args.name is None) and args.number):      
            if(args.number):
                    temp = int(args.number)
            else:
                    temp = 1
            i=0
            while i < temp:
                container_name = CM.ct_list[CM.ct_number-1-i][0]
                ##  the stop process starts from the end of the container list
                ##  the start process starts from the end of the container list
                try:
                    start_container = CM.client.containers.get(container_name)
                    start_container.start()
                    CM.do_refresh(self)
                    CM.do_writefile(self)
                    i = i + 1
                except docker.errors.NotFound as e:
                    print("container not found when starting containers:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when starting containers:\n", e)
        CM.do_list_container(self,line=None)
##
    def do_create_container(self, line):
        CM.do_refresh(self)
        CM.do_writefile(self)       
        parser = argparse.ArgumentParser()
        parser.add_argument('-number', help='Specify the number')
        parser.add_argument('-image', help='Specify an image')
        args = parser.parse_args(shlex.split(line))

        if(args.number):
            temp = int(args.number)
        else:
            temp = 1
        i = 0
        temp2=0

        if(args.image):
            container_image=args.image
        else:
            container_image='cm-client'

        while i < temp:
            temp2 = temp2 + 1        
            container_name = f"container{temp2}"
            try:    
                ##  the only valid option for creating containers
                CM.client.containers.create(image=container_image, name=container_name,command='sh',detach=True,stdin_open=True,tty=True)
                CM.do_refresh(self)
                CM.do_writefile(self)                    
                i = i + 1
            except docker.errors.APIError as e:
                if(e.status_code == 409):
                    ##  which means the name of the container is already occupied
                    ##  the cluster manager should try another name
                    continue
                else:   
                    ##  unexpected error occured when creating containers
                    print("an error occured when creating containers:\n", e)
            except docker.errors.ImageNotFound as e:
                print("an error occured when creating containers:\n", e)        
        CM.do_list_container(self,line=None)


##
    def do_exec_command_container(self,line):
        CM.do_refresh(self)
        CM.do_writefile(self)     
        parser = argparse.ArgumentParser()
        parser.add_argument('-number', help='Specify the number')
        parser.add_argument('-name', help='Specify a name')
        parser.add_argument('-command', type=str,help='Specify a command')
        args = parser.parse_args(shlex.split(line))

        if(args.name and args.number):
                print(f'please enter either a name or a number')
        elif((args.name is None) and (args.number is None)):
                print(f'please enter either a name or a number')
        elif(args.name and (args.number is None)):
                container_name = args.name
                try:
                    exec_container = CM.client.containers.get(container_name)
                    exec_container.start()
                    exec_result = exec_container.exec_run(cmd=args.command)

                    print(f"{container_name}")
                    exit_code = exec_result.exit_code
                    print(f"Command Exit Code:\n{exit_code}")
                    output = exec_result.output
                    print(f"Command Output:\n{output}")
                    logs = exec_container.logs()
                    print(f"Container Logs\n:{logs}")
                except docker.errors.NotFound as e:
                    print("container not found when executing commands:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when executing commands:\n", e)            
        elif((args.name is None) and args.number):      
            if(args.number):
                    temp = int(args.number)
            else:
                    temp = 1
            i=0
            while i < temp:
                container_name = CM.ct_list[CM.ct_number-1-i][0]
                try:
                    exec_container = CM.client.containers.get(container_name)
                    exec_container.start()
                    exec_result = exec_container.exec_run(cmd=args.command)

                    print(f"{container_name}")
                    exit_code = exec_result.exit_code
                    print(f"Command Exit Code:\n{exit_code}")
                    output = exec_result.output
                    print(f"Command Output:\n{output}")
                    logs = exec_container.logs()
                    print(f"Container Logs\n:{logs}")
           
                    i = i + 1
                except docker.errors.NotFound as e:
                    print("container not found when executing commands:\n",e)
                except docker.errors.APIError as e:
                    print("an error occured when executing commands:\n", e)
##
    def do_quit(self, line):
        return True  # 退出程序
##
    def do_assignment2(self,line):  
        parallel_n=4

        ##   random_numbers = np.random.randint(1, 101, size=100000)
        ##   np.save('random_numbers.npy', random_numbers)
        random_numbers=np.load('random_numbers.npy')

        for i in range(parallel_n):
            image_name = 'cm-client'
            container_name = f'container4parallelprocessing{i+1}'
            vol_name ='volume4parallelprocessing'
            tar_path = '/app'
            mount_config = docker.types.Mount(source=vol_name,target=tar_path,type='volume')
            hostname = f'{i+1}'

            ##  some very important setting about the container is done by customizing the image
            ##  written in the dockerfile
            container = CM.client.containers.run(image=image_name, name=container_name,
                                                    detach=True,stdin_open=True,tty=True,
                                                    mounts=[mount_config],hostname=hostname)
            response = container.exec_run(cmd="python miniproject2_client.py")
            print("/------------------------------------/")
            print("Container:",container_name)
            exit_code = response.exit_code
            print("Exit code:", exit_code)
            output = response.output.decode()
            print("Output:\n", output)
##  the function is not ideal, since it is programmed in blocking statements.
##  therefore, another container will not be started,until the former one returns its value of executed commands
##  (response = container.exec_run(cmd="python miniproject2_client.py") is a very typical blocking statement)
##  setting up a real parallel data processing, in my perspective, requires non-blocking statements,like what Verilog HDL does
##  based on my initial investigation, it is possible to build non-blocking statements in python.
##  unfortunately, i do not have enough time to work further on it,
##  not only because the work is time-consuming, but it is also away from our topic

####
    def do_assignment3(self,line):  

        np.random.seed(101)
        # Generating random linear data
        # There will be 50 data points ranging from 0 to 50
        x = np.linspace(0, 50, 50)
        y = np.linspace(0, 50, 50)
        # Adding noise to the random linear data
        x += np.random.uniform(-5, 5, 50)
        y += np.random.uniform(-5, 5, 50)
        np.save('x4linear_regression.npy', x)
        np.save('y4linear_regression.npy', y)

        image_name = 'cm-client'
        container_name = f'container4linearregression'
        vol_name = f'volume4linearregression'
        tar_path = '/app'
        mount_config = docker.types.Mount(source=vol_name,target=tar_path,type='volume')
        hostname = f'1'
        ##  some very important setting about the container is done by customizing the image
        ##  written in the dockerfile
        container = CM.client.containers.run(image=image_name, name=container_name,
                                             detach=True,stdin_open=True,tty=True,
                                             mounts=[mount_config],hostname=hostname)
        response = container.exec_run(cmd="python miniproject3_client.py")
        print("/------------------------------------/")
        print("Container:",container_name)
        exit_code = response.exit_code
        print("Exit code:", exit_code)
        output = response.output.decode()
        print("Output:\n", output)


##
if __name__ == "__main__":
    os.system('cls')
    my_cmd = CM()
    my_cmd.cmdloop()  # 运行命令行解释器
