from mod_python import apache
from mod_python import util
import commands
def index(req):
    return "we are in index"
def jump2(req):
    (status,output)=commands.getstatusoutput('/var/www/script/addUser.sh Jane 123 2.htpasswd')

    #return output
    if status==0:
        util.redirect(req,"/FlowControl/2.html")
    return apache.OK
def jump3(req):
    (status,output)=commands.getstatusoutput('/var/www/script/addUser.sh Jane 123 3.htpasswd')
    #return output
    if status==0:
        util.redirect(req,"/FlowControl/3.html")
    return apache.OK

def jump4(req):
    (status,output)=commands.getstatusoutput('/var/www/script/addUser.sh Jane 123 4.htpasswd')
    if status==0:
        (status,output)=commands.getstatusoutput('/var/www/script/removeUser.sh Jane 2.htpasswd')
        (status,output)=commands.getstatusoutput('/var/www/script/removeUser.sh Jane 3.htpasswd')
        util.redirect(req,"/FlowControl/4.html")
    return apache.OK

