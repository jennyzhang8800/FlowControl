# -*- coding: utf-8 -*-
import pkg_resources

from xblock.core import XBlock
from xblock.fields import Scope, Integer,String
from xblock.fragment import Fragment
from conf import Config
from util import Util
from GitRepo import GitRepo
import logging
import datetime
import sys
import codecs
import json
import hashlib
import urllib2
import base64
import pymongo
import os
class WorkflowXBlock(XBlock):
    """
    这是一个工作流测试的xblock
    """

    # Fields are defined on the class.  You can access them in your code as
    # self.<fieldname>.

    # TO-DO: delete count, and define your own fields.

    logger = Util.logger(Config.loggerConfig)
    gitlabRepo = GitRepo(dict(Config.teacherGitlab, **{'logger': logger}))
	
    count = Integer(
        default=0, scope=Scope.user_state,
        help="A simple counter, to show something happening",
    )
    display_name = String(
        display_name="Display name",
        help="This is a workflow test block",
        scope=Scope.settings,
        default='工作流',
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    # TO-DO: change this view to display your data your own way.
    def student_view(self, context=None):
        """
        The primary view of the WorkflowXBlock, shown to students
        when viewing courses.
        """
        html = self.resource_string("static/html/workflow.html")
        frag = Fragment(html.format(self=self))
        frag.add_css(self.resource_string("static/css/workflow.css"))
        frag.add_javascript(self.resource_string("static/js/src/workflow.js"))
        frag.initialize_js('WorkflowXBlock')
        return frag

    # TO-DO: change this handler to perform your own actions.  You may need more
    # than one handler, or you may not need any handlers at all.
  
    @XBlock.json_handler
    def submit(self,data,suffix=''):
        """提交本章所有练习"""
        student = self.runtime.get_real_user(self.runtime.anonymous_student_id)
        studentEmail = student.email
        #get all quizzes qNo attribute of current chapter
        #获取本章所有练习题号
        chapter = self.get_parent().get_parent().get_parent()
        subsections = chapter.get_children()
        qNo_list=[]
        for subsection in subsections:
            for unit in subsection.get_children():
                for xblock in unit.get_children():
                    if hasattr(xblock, "qNo"):
                        qNo_list.append({'qNo':xblock.qNo,'subsection':subsection.display_name,'url_name':subsection.url_name})
        self.logger.info("email=%s,chapter_display_name=%s,submit this chapter",studentEmail,chapter.display_name)
        #check if all of the quizzes of this chapter have already been submmited?
        #fetch answer Info from gitlab
        #从gialb获取本章所有未提交的练习题号
        unSubmitList=[]
        for item in qNo_list:
            tried,answerList = self.fetchAnswerInfo(student,item['qNo'])
            item['tried']=tried
            if int(tried)==0:
                unSubmitList.append(item)
        #self.logger.info('unSubmitList=%s',unSubmitList)
        # all of the quizzes of this chapter have already been submmited
        #如果所有题己提交
        if len(unSubmitList)==0:	
            cur_href=data['cur_href']
            href_splited= cur_href.split('/')
            for index,item in enumerate(href_splited):
                if item =='courseware':
                    url_name = href_splited[index+1]
                    break
            #connect to  mongodb 'workflow'collection
            conn = pymongo.Connection('localhost', 27017)
            db = conn.test
            db.authenticate("edxapp","p@ssw0rd")
            result = db.workflow.find_one({'email':studentEmail}) #connect to collection
            #更新MongoDB,开启下一章
            if result:
                for index,item in enumerate(result['workflow']):
                    if item['url_name'] == url_name:
                        result['workflow'][index+1]['visible']=True
                        next_url_name = result['workflow'][index+1]['url_name']
                        break
                db.workflow.update({"email":studentEmail},{"$set":{"workflow":result['workflow']}})
                next_url = cur_href.split('courseware')[0]+'courseware/'+next_url_name
            else:
                next_url = cur_href
            conn.disconnect()
            #调用批改脚本
            try:
                status1=os.system('/var/www/zyni/script/pullFromGitlab.sh')
                status2=os.system('python /var/www/data/answer/tool/grade.py -s '+student.username)
                status3=os.system('/var/www/zyni/script/pushToGitlab.sh grade')
                self.logger.info("grade.py -s %s status1=%s,status2=%s,status3=%s",studentEmail,status1,status2,status3)
            except Exception as e:
                self.logger.exception('ERROR: workflow.py %s' % (str(e)))         
            return {'url_name':next_url,'email':studentEmail,'unSubmitList':unSubmitList}
        #还有题没有提交
        else:
            self.logger.info('submit chapter fail,because there are unSubmited quizzes.')
            return {'url_name':data['cur_href'],'email':studentEmail,'unSubmitList':unSubmitList}            
     

    def fetchAnswerInfo(self, student, qNo):
        '''
        从gitlab获取学生的回答信息,并保存
        '''
        filepath = '%(emailHash)s/%(username)s/%(qNo)d/%(qNo)d.json' % {
            'emailHash': hashlib.new('md5', student.email).hexdigest()[-2:],
            'username': student.username,
            'qNo': qNo
        }
        answerInfo = self.gitlabRepo.readContent(filepath)
        if answerInfo is None:
            return (0, [])
        else:
            self.logger.info('fetch answer info from gitlab')
            return (answerInfo['tried'], answerInfo['answer'])


    # TO-DO: change this to create the scenarios you'd like to see in the
    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("WorkflowXBlock",
             """<workflow/>
             """),
            ("Multiple WorkflowXBlock",
             """<vertical_demo>
                <workflow/>
                <workflow/>
                <workflow/>
                </vertical_demo>
             """),
        ]
