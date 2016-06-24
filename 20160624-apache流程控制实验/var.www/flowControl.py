from mod_python import apache
from mod_python import util
def handler(req):
    req.content_type='text/plain'
    form = util.FieldStorage(req)
    page=form.list[0]
    if page=="1.html":
        util.redirect(req,'1.html')
    elif page=="2.html":
        util.redirect(req,'2.html')
    elif page=="3.html":
        util.redirect(req,'3.html')
    elif page=="4.html":
        util.redirect(req,'4.html')
    else:
        req.write("Bad Page!")
    
    return apache.OK
