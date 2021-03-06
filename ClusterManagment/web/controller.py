#encoding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import web
import helper
from web import form
from listen import Listen
render = web.template.render('templates/' , base='layout')
urls = (
        '/addscript2group' , 'add2group',
        '/addserver2group' , 'add2group',
        '/addservice2group','add2group',
         '/addtask2service','addtask2service',
        '/deletescript' , 'delete',
        '/deleteserver' , 'delete',
        '/deleteservice' , 'delete',
        '/removescript', 'remove',
        '/removeserver', 'remove',
        '/removeservice','remove',
        '/get_info','get_info',
        '/init_info','init_info',
        '/','about',
        '/show','show',
        '/(.*)','index',

    
)
class show:
    def GET(self,):
        res=helper.getallshow()
        
        return render.show(res)

class init_info:
    def GET(self,):
        ip=web.input()['ip']
        info=Listen.get_all_info(ip)
        if info==None:return None
        return info

class get_info:
    def GET(self,):
        ip=web.input()['ip']
        info=Listen.get_lastest_info(ip)
        if info==None:
            return None
        info=list(eval(info))
        info[2]=list(info[2])
        return info

def get_result_alert(flag) :
    alert_text ="""
        <div class='alert alert-%s'>
            <button type='button' class='close' data-dismiss='alert'>x</button>
            <strong>%s</strong> %s
        </div>
        """ 
    if flag == 'success' :
        return alert_text % (flag , 'Success' , 'Right , Just do it !')
    elif flag == 'error' :
        return alert_text % (flag , 'Error' , 'Fail , Please Check!')
    else :
        return ""

def get_result_alert2(flag , title , msg) :
    alert_text ="""
        <div class='alert alert-%s'>
            <button type='button' class='close' data-dismiss='alert'>x</button>
            <strong>%s</strong> %s
        </div>
        """ 
    return alert_text % (flag , title , msg)
class index :
    templates = ['add_server' , 'add_script' , 'add_service','manage_server' , 'manage_script' , 'manage_task' , 'edit_server' , 'edit_script','manage_serverGroup','manage_scriptGroup','manage_service','server_info']
    def GET(self , template_name):

        if self.templates.count(template_name) <= 0 :
            return "404"

        render_template = 'render._' + str(template_name)
        foo = eval(render_template)
        if template_name == 'server_info' :
            ip= web.input()['ip']
            return foo(ip)

        elif template_name == 'manage_script' :
            i = web.input(group_id='0', res='None')
            current_group = None
            if i['group_id'] == None or i['group_id'] == '0' :
                script_list = helper.get_all_scripts()
            else :
                script_list = helper.get_scripts_by_group_id(i['group_id'])
                current_group = helper.get_script_group_by_id(i['group_id'])
            group_list = helper.get_script_group_list()
            if group_list['val'] == None :
                group_list['val'] = []
            if script_list['val'] == None :
                script_list['val'] = []

            return foo({"scripts_list" : script_list['val'] , "group_list" : group_list['val'] , "group" : current_group , "result" :get_result_alert(i['res'])})
        elif template_name == 'manage_server' :
            i = web.input(group_id='0' , res='None')
            current_group = None
            if i['group_id'] == None or i['group_id'] == '0' :
                server_list = helper.get_all_servers()
            else :
                server_list = helper.get_servers_by_group_id(i['group_id'])
                current_group = helper.get_server_group_by_id(i['group_id'])
            group_list = helper.get_server_group_list()
            if group_list['val'] == None :
                group_list['val'] = []
            if server_list['val'] == None :
                server_list['val'] = []
            return foo({"servers_list" : server_list['val'] , "group_list" : group_list['val'] , "group" : current_group , "result" : get_result_alert(i['res'])})

        elif template_name=='manage_serverGroup':
            i=web.input(res='None')
            server_group_list=helper.get_server_group_list()
            if server_group_list["status"] == -1 or server_group_list["val"] == None :
                server_group_list['val']=[]
            if i['res']=='None':
                return foo({"group_list":server_group_list['val'],"result":''})
            elif i['res']=='deleteserverGroupsucess':
                return foo({"group_list":server_group_list['val'],"result" : get_result_alert('success')})

            return foo({"group_list":server_group_list['val'],"result" : get_result_alert2('warming','Warming',i['res'])})
        elif template_name=='manage_scriptGroup':
            i=web.input(res='None')
            script_group_list=helper.get_script_group_list()
            if script_group_list["status"] == -1 or script_group_list["val"] == None:
                script_group_list['val']=[]
            if i['res']=='None':
                return foo({"group_list":script_group_list['val'],"result":''})
            elif i['res']=='deleteserverGroupsucess':
                return foo({"group_list":script_group_list['val'],"result" : get_result_alert('success')})
            return foo({"group_list":script_group_list['val'],"result" : get_result_alert2('warming','Warming',i['res'])})
        

        elif template_name == 'add_script':
            i = web.input(res='None')
            if i['res']== 'success' :
                return foo({"result":get_result_alert2('success','Success','Add a new script(group)')})
            elif i['res'] == 'error' :
                return foo({"result":get_result_alert2('error','Error','Fail to add script(group)')})
            else :
                return foo({"result":""})
        elif template_name == 'add_server':
            i = web.input(res='None')
            if i['res']== 'success' :
                return foo({"result":get_result_alert2('success','Success','Add a new server(group)')})
            elif i['res'] == 'error' :
                return foo({"result":get_result_alert2('error','Error','Fail to add server(group)')})
            else :
                return foo({"result":""})
        elif template_name == 'add_service':
            i = web.input(res='None')
            if i['res']== 'success' :
                return foo({"result":get_result_alert2('success','Success','Add a new service')})
            elif i['res'] == 'error' :
                return foo({"result":get_result_alert2('error','Error','Fail to add service')})
            else :
                return foo({"result":""})

        elif template_name == 'manage_service' :
            i = web.input(group_id='0' , res='None')
            current_group = None
            tasks=helper.get_all_tasks()

            if i['group_id'] == None or i['group_id'] == '0' :
                service_list = helper.get_all_service()
            else :
                service_list = helper.get_services_by_group_id(i['group_id'])
                current_group = helper.get_server_group_by_id(i['group_id'])
            group_list = helper.get_server_group_list()

            if group_list['val'] == None :
                group_list['val'] = []
            if service_list['val'] == None :
                service_list['val'] = []
            if tasks['val']==None:
                tasks['val']=[]
            return foo({"services_list" : service_list['val'] , "task_list":tasks['val'],"group_list" : group_list['val'] , "group" : current_group , "result" : get_result_alert(i['res'])})

        elif template_name == 'edit_script' :
            i = web.input(res=None)
            script_id = i['script_id']
            script = helper.get_script_by_id(script_id)["val"]
            script_content = helper.get_script_content_by_id(script_id)["val"]
            args = {}
            args["script_id"] = script_id
            args["script"] = script
            args["content"] = script_content
            if i['res']== 'success' :
                args["result"] = get_result_alert2('success','Success','Update script(group) successfully!')
            elif i['res'] == 'error' :
                args["result"] = get_result_alert2('error','Error','Fail to update script(group)')
            else :
                args["result"] = ''
            return foo(args)
        elif template_name == 'edit_server' :
            i = web.input(res=None)
            server_id = i["server_id"]
            server = helper.get_server_by_id(server_id)["val"]
            args = {}
            args["server"] = server
            if i['res']== 'success' :
                args["result"] = get_result_alert2('success','Success','Update server(group) successfully!')
            elif i['res'] == 'error' :
                args["result"] = get_result_alert2('error','Error','Fail to update server(group)')
            else :
                args["result"] ='' 
            return foo(args)

        elif template_name == 'manage_task' :
            i =web.input(res=None,service_id=None)
            args = {}
            server_group_list = helper.get_server_group_list()
            script_group_list = helper.get_script_group_list()
            if server_group_list["status"] == -1 or server_group_list["val"] == None :
                server_group_list = []
            else:
                server_group_list = server_group_list["val"]
            if script_group_list["status"] == -1 or script_group_list["val"] == None :
                script_group_list = []
            else:
                script_group_list = script_group_list["val"]
            if i["service_id"]!=None:
                task_list_res=helper.get_tasks_by_serviceid(i["service_id"])
            else:
                task_list_res = helper.get_all_tasks()
            if task_list_res["status"] == -1 or task_list_res["val"] == None :
                task_list = []
            else :
                task_list = task_list_res["val"]
            args["server_group_list"] = server_group_list
            args["script_group_list"] = script_group_list
            args["task_list"] = task_list
            args["result"] = ""
            if i['res'] != None:
                if i['res'] == 'notstart' :
                    args["result"] = get_result_alert2('error' , 'Waring' , 'Task has not started!')
                elif i['res'] == 'runerror' :
                    args["result"] = get_result_alert2('error' , 'Waring' , 'Exception occurs when run task , server group and script group can not be empty , check!')
                elif i['res'] == 'runsuccess' :
                    args["result"] = get_result_alert2('success' , 'Success' , 'Task start ! Please click ViewStatus button to view scripts status')
                elif i['res'] == 'addtasksuccess' :
                    args["result"] = get_result_alert2('success' , 'Success' , 'A new Task created! ')
                elif i['res'] == 'addtaskerror' :
                    args["result"] = get_result_alert2('error' , 'Error' , 'Fail to Create task , please check!')
                elif i['res'] == 'deletetasksuccess' :
                    args["result"] = get_result_alert2('success','Success' , 'The task has been deleted successfullly')
                elif i['res'] == 'deletetaskerror' :
                    args["result"] = get_result_alert2('error' , 'Error' , 'Fail to delete task , please check!')
            return foo(args)
        else :
            return "404"


    def do_with_view_status (self, task_id , status_res) :
        args = {}
        server_group_list = helper.get_server_group_list()
        script_group_list = helper.get_script_group_list()
        if server_group_list["status"] == -1 or server_group_list["val"] == None :
            server_group_list = []
        else:
            server_group_list = server_group_list["val"]
        if script_group_list["status"] == -1 or script_group_list["val"] == None :
            script_group_list = []
        else:
            script_group_list = script_group_list["val"]
        
        task_list_res = helper.get_all_tasks()
        if task_list_res["status"] == -1 or task_list_res["val"] == None :
            task_list = []
        else :
            task_list = task_list_res["val"]
        
        current_task = helper.get_task_by_id(task_id)["val"]
        status_list = []
        scripts_length = len(current_task["script_group"].scripts)
        for server in current_task["server_group"].servers :
            status = {}
            status["username"] = server.username
            status["host_address"] = server.host_address
            if status_res.has_key(server.id) == False :
                status["console_output"] = ""
                status["final_status"] = -2
                script_status = []
                for i in range(scripts_length) :
                    script_status.append(-1)
                status["script_status"] = script_status
                status_list.append(status)
                continue

            status["console_output"] = status_res[server.id]["content"]
            status["final_status"] = status_res[server.id]["status"]
            script_status = []
            if status_res[server.id].has_key("executing_id") == True :
                for i in range(scripts_length) :
                    if i == status_res[server.id]["executing_id"] :
                        if status_res[server.id]["status"] >=0:
                            script_status.append(1)
                        else :
                            script_status.append(-1)
                    elif i > status_res[server.id]["executing_id"] :
                        script_status.append(2)
                    else :
                        script_status.append(0)
            else :
                for i in range(scripts_length) :
                    script_status.append(-1)
            if status_res[server.id]["status"] == 0 :
                script_status = []
                for i in range(scripts_length) :
                    script_status.append(0)
            status["script_status"] = script_status
            status_list.append(status)
            print status_list
        current_scripts = helper.get_scripts_by_group_id(current_task["script_group"].id)["val"]
        args["server_group_list"] = server_group_list
        args["script_group_list"] = script_group_list
        args["task_list"] = task_list
        args["result"] = ""
        args["current_scripts"] = current_scripts
        args["status_list"] = status_list
        args["current_task_id"] = task_id
        return render._view_status(args)

    def POST(self , action_name):
        ''' 所有的表单处理都，在一个post方法里。通过传递form里的action所对应的值，来确定是哪个表单，和get一样，post方法同样在参数里             捕捉剩余的url。
        '''
        post_data = web.input()
        
        if action_name == 'add_server' :
            add_server_res = helper.create_server(str(post_data['user_name']) , str(post_data['user_password']) , str(post_data['host_address']) , str(post_data['host_port']) , str(post_data['script_path']))
            if add_server_res['status'] == 0 :
                raise web.seeother('/add_server?res=success')
            else :
                raise web.seeother('/add_server?res=error')
        elif action_name == 'add_server_group' :
            add_server_group_res = helper.create_servergroup(str(post_data['server_groupname']))
            if add_server_group_res['status'] == 0 :
                raise web.seeother('/add_server?res=success')
            else :
                raise web.seeother('/add_server?res=error')
        elif action_name == 'add_script' :
            add_script_res = helper.create_script(str(post_data['script_name']) , str(post_data['script_content']) , str(post_data['script_desc']))
            if add_script_res['status'] == 0 :
                raise web.seeother('/add_script?res=success')
            else :
                raise web.seeother('/add_script?res=error')
        elif action_name == 'update_script' :
            update_script_res = helper.update_script(post_data['script_id'] , str(post_data['script_name']) , str(post_data['script_content']) , str(post_data['script_desc']))
            script_id = str(post_data['script_id'])
            if update_script_res['status'] == 0 :
                raise web.seeother('/edit_script?res=success&script_id='+script_id)
            else :
                raise web.seeother('/edit_script?res=error&script_id='+script_id)
        elif action_name == 'update_server' :
            update_server_res = helper.update_server(post_data['server_id'] , str(post_data['user_name']) , str(post_data['user_password']) , str(post_data['host_address']) , str(post_data['host_port']) , str(post_data['script_path']))
            server_id = str(post_data['server_id'])
            if update_server_res['status'] == 0 :
                raise web.seeother('/edit_server?res=success&server_id='+server_id)
            else :
                raise web.seeother('/edit_server?res=success&server_id='+server_id)

        elif action_name == 'add_service':
            add_service_res = helper.create_service(str(post_data['service_name']) , str(post_data['service_desc']))
            if add_service_res['status'] == 0:
                raise web.seeother('/add_service?res=success')
            else :
                raise web.seeother('/add_service?res=error')
        elif action_name == 'update_script':
            update_script_res = helper.update_service(post_data['service_id'] , str(post_data['service_name']) , str(post_data['service_desc']))
            service = str(post_data['script_id'])
            if update_service_res['status'] == 0 :
                raise web.seeother('/edit_service?res=success&script_id='+script_id)
            else :
                raise web.seeother('/edit_service?res=error&script_id='+script_id)

        elif action_name == 'add_script_group' :
            add_script_group_res = helper.create_scriptgroup(str(post_data['script_groupname']))
            if add_script_group_res['status'] == 0 :
                raise web.seeother('/add_script?res=success')
            else :
                raise web.seeother('/add_script?res=error')
        elif action_name == 'update_position' :
            update_position_res = helper.update_position( post_data['current_group_id'] , post_data['sort_list'] )
            group_id = post_data['current_group_id']
            if update_position_res['status'] == 0 :
                raise web.seeother('/manage_script?res=success&group_id='+str(group_id))
            else :
                raise web.seeother('/manage_script?res=success&group_id='+str(group_id))
        elif action_name == 'view_status' :
            task_id = post_data["task_id"]
            request_res = helper.do_request(task_id)
            print request_res
            if request_res["status"] == -1 :
                raise web.seeother('manage_task?res=notstart')
            count=0
            for i in request_res['val'].values():
                i['content']=request_res['val'].values()[count]['content'].replace('\r\n','<br/>')
                count+=1
            return self.do_with_view_status( task_id , request_res["val"]) 
        elif action_name == "run_task" :
            task_id = post_data["task_id"]
            run_res = helper.do_command(task_id)
            if run_res["status"] == -1 :
                raise web.seeother('manage_task?res=runerror')
            return web.seeother('manage_task?res=runsuccess')
        elif action_name == "add_task" :
            script_group_id = post_data["select_script_group"]
            server_group_id = post_data["select_server_group"]
            task_name = post_data["task_name"]
            task = helper.create_task(task_name , script_group_id , server_group_id)
            if task["status"] == 0 :
                raise web.seeother("manage_task?res=addtasksuccess")
            else :
                raise web.seeother("manage_task?res=addtaskerror")
        elif action_name == "delete_task":
            delete_res = helper.delete_task(post_data["task_id"])
            if delete_res["status"] == 0:
                raise web.seeother("manage_task?res=deletetasksuccess")
            else :
                raise web.seeother("manage_task?res=deletetaskerror")
        elif action_name == 'delete_serverGroup':
            delete_res=helper.delete_serverGroup(post_data['serverGroup_id'])
            if delete_res["status"] == 0:
                raise web.seeother("manage_serverGroup?res=deleteserverGroupsucess")
            else :
                raise web.seeother("manage_serverGroup?res=%s"%(delete_res['val']))

        elif action_name == 'delete_scriptGroup':
            delete_res=helper.delete_scriptGroup(post_data['scriptGroup_id'])
            if delete_res["status"] == 0:
                raise web.seeother("manage_scriptGroup?res=deleteserverGroupsucess")
            else :
                raise web.seeother("manage_scriptGroup?res=%s"%(delete_res['val']))

            
def redirect2home(flag , category , group_id = 0) :
    if category == 'script':
        if flag == 0 :
            raise web.seeother('/manage_script?res=success&group_id='+str(group_id))
        else :
            raise web.seeother('/manage_script?res=error&group_id='+str(group_id))
    elif category == 'server' :
        if flag == 0 :
            raise web.seeother('/manage_server?res=success&group_id'+str(group_id))
        else :
            raise web.seeother('/manage_server?res=success&group_id'+str(group_id))
    elif category == 'service' :
        if flag == 0 :
            raise web.seeother('/manage_service?res=success&group_id'+str(group_id))
        else :
            raise web.seeother('/manage_service?res=success&group_id'+str(group_id))

    else :
        raise web.seeother('/') 
    

class add2group :
    def GET(self) :
        input_args = web.input()
        category = input_args['category']
        if category == 'script' :
            res = helper.add_script2group(str(input_args['script_id']) , str(input_args['group_id']))
            return redirect2home(res['status'] , 'script' , str(input_args['current_group_id']))
        elif category == 'server' :
            res = helper.add_server2group(str(input_args['server_id']) , str(input_args['group_id']))
            return redirect2home(res['status'] , 'server' , str(input_args['current_group_id']))
        elif category=='service':
            res = helper.add_service2group(str(input_args['service_id']) , str(input_args['group_id']))
            return redirect2home(res['status'] , 'service' , str(input_args['current_group_id']))
        else :
            return "404"
class addtask2service:
    def GET(self,):
        input_args=web.input()
        res=helper.add_task2service(str(input_args['task_id']),str(input_args['service_id']))
        return redirect2home(res['status'] , 'service' , str(input_args['current_group_id']))
class delete :
    def GET(self) :
        input_args = web.input()
        category = input_args['category']
        if category == 'script' :
            res = helper.delete_script(str(input_args['script_id']))
            return redirect2home(res['status'] , 'script' , str(input_args['current_group_id']))
        elif category == 'server' :
            res = helper.delete_server(str(input_args['server_id']))
            return redirect2home(res['status'] , 'server' , str(input_args['current_group_id']))
        elif category == 'service' :
            res = helper.delete_service(str(input_args['service_id']))
            return redirect2home(res['status'] , 'service' , str(input_args['current_group_id']))
        else:
            return "404"


class remove :
    def GET(self) :
        input_args = web.input()
        category = input_args['category']
        if category == 'script':
            res = helper.remove_script(str(input_args['script_id']) , str(input_args['group_id']))
            return redirect2home(res['status'] , 'script' , str(input_args['current_group_id']))
        elif category == 'server':
            res = helper.remove_server(str(input_args['server_id']) , str(input_args['current_group_id']))
            return redirect2home(res['status'] , 'server' , str(input_args['current_group_id']))
        elif category == 'service':
            res = helper.remove_service(str(input_args['service_id']) , str(input_args['current_group_id']))
            return redirect2home(res['status'] , 'service' , str(input_args['current_group_id']))

        else :
            return "404"

class about :
    def GET(self,) :
        return render._home()

if __name__ == '__main__' :
    app = web.application(urls,globals())
    app.run()
