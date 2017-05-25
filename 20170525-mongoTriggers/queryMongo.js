/**
 * 
 */

var mongojs = require('mongojs');

var db = mongojs('localhost/test', ['workflow']);
var coll = db.collection('workflow');
//db.workflow.save({email:'tom@163.com'});
//db.workflow.findOne({'email':'jennyzhang8800@163.com'},function(err,doc){console.log(doc.email.toString())});

var triggers = require('./index.js');

/*
triggers(db.workflow).insert(
    function(document, next) {
        if(document.name = "Iddo Gino")
            next("Exists");
        else{
           console.log('next');
            next();
    }
}
);

*/
triggers(db.workflow).on('insert', function(err,res,query,update,ops) {
    console.log('saved');
  //  console.log(err);
    
    console.log(query)
   // console.log(update);
   // console.log(ops);
});

db.workflow.insert({email:'tt@126.com'})
//db.workflow.save({name:"Iddo Gino", password:"Hard2Crack"}, function(err, res) {
//    if(err)
//        console.log(err);
//    console.log("Saved!");
//});

