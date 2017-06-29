/* Javascript for WorkflowXBlock. */
function WorkflowXBlock(runtime, element) {
       
    //添加“下一题”按钮
    function jumpToXblock(result){
        root = result.root;  
        lms_web_url = result.blocks[root].lms_web_url;
        window.location.href=lms_web_url;
    }
        //调用XBLOCK API，根据xlbock_id获取该xblock的信息（包括 lms访问链接）
    function submitSuccess(result){
       var unSubmitList = result.unSubmitList;
        if(unSubmitList.length == 0){
          alert("您己完成本章所有练习！");
          window.location.href=result.url_name;
        } 
        else{
           onLoadTable(unSubmitList);

        }
        
    }

    var handlerUrlSubmit = runtime.handlerUrl(element,'submit');

    //点击提交按钮，从后台获得course_id和下一题的xlbock_id信
    //然后调用submitSuccess信息息
    $('#submit', element).click(function(eventObject) {

      var cur_href=window.location.href;
      $.ajax({
            type: "POST",
            url: handlerUrlSubmit,
            data: JSON.stringify({"cur_href":cur_href}),
            success: submitSuccess
        });
    });
    function onLoadTable(unSubmitList){
            $("#reMsg",element).html("");
            var p = $("<p style='color:red; align:center;'>提交失败！请先完成本章所有练习！ </p>");
            p.appendTo($("#reMsg",element));
            var table =$( "<table class='altrowstable' id='tableFirst align='center' width='100%'>");
            table.appendTo($("#reMsg",element));
            var caption =$("  <caption style='font-size:20px;font-weight:bold' >"+"您有"+unSubmitList.length+"个未提交的题</caption>")
            caption.appendTo(table);
            var thread = $(" <thead><tr><th id='Index' >序号</th><th id='postion' >位置</th></tr></thead>");
            thread.appendTo(table);
            for(var i=0;i<unSubmitList.length;i++){
                var tr=$("<tr></tr>");
                tr.appendTo(table);

                var td=$("<td>"+(i+1)+"</td>");
                td.appendTo(tr);
                var cur_href = window.location.href
                var splited_href = cur_href.split('courseware')[0]
                var chapter_url_name = cur_href.split('courseware')[1].split('/')[1]
                
                var next_url = splited_href+'courseware/'+chapter_url_name+"/"+unSubmitList[i]['url_name']
                var td=$("<td><a href="+next_url+">"+unSubmitList[i]['subsection']+"</a></td>");
                td.appendTo(tr);

            }
            $("#reMsg",element).append("</table>");
    }


    $(function ($) {
        /* Here's where you'd do things on page load. */
    });
}
