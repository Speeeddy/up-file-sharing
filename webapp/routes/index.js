var express = require('express');
var router = express.Router();
var https = require('https');
var multer  = require('multer')
var upload = multer({ dest: './public' })
var fs = require('fs');



router.get('/', function(req, res, next) {
	if(typeof(req.session.login)=="undefined"||req.session.login==0){
		console.log(req.session.login);
		res.render('login',{e:"0"});
	}
	else{
		console.log(req.session.login);
		 res.redirect('/index');
	}
  
});





router.get('/reg', function(req, res, next) {
res.render("reg",{e:"0"});
});




router.post('/reg', function(req, res, next) {
 var dat={
	"username":req.body.uname,
	"password": req.body.pswd,
	"name":req.body.rname,
	"number":req.body.number,
	"email":req.body.email
}
  var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/um/register',
	method: 'POST'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(res) => {
  console.log(`statusCode: ${res.statusCode}`)
  res.on('data', (d) => {
    console.log("test"+d.toString("utf8"));
   if(JSON.parse(d.toString())=="User Created"){

   resp.redirect("/")

   }else{
   	resp.render("reg",{e:"1"})
   }
  })
  res.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()

});


router.get("/logout",function(req, res, next){
req.session.login=0;
res.render('login',{e:"0"});
})



router.get('/index', function(req, res, next) {
  	if(typeof(req.session.login)=="undefined"||req.session.login==0){
		res.redirect('/');
	}
  res.render('index',{name:req.session.username});
});

router.post('/login', function(req, res, next) {
	console.log(req.session.login);
   if(typeof(req.session.login)=="undefined"||req.session.login==0){

 var dat={
	"username":req.body.uname,
	"password": req.body.pswd
}
  var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/um/login',
	method: 'POST'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(res) => {
  console.log(`statusCode: ${res.statusCode}`)
  res.on('data', (d) => {
    console.log("test"+d.toString("utf8"));
    if(JSON.parse(d.toString())=="Verified"){
    	console.log("logged in")
   req.session.username=req.body.uname;
   req.session.login=1
   resp.redirect('/index');
    }
    else{ console.log("incorrect")
    	 req.session.login=0;
    	resp.render('login',{e:"1"});
    }
  })
  res.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()

  }
});


router.post('/receivernameverification',function(req,res)  {

 var dat={
	"username":req.body.receiver
}
  var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/um/check',
	method: 'POST'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(resp) => {
  console.log(`statusCode: ${res.statusCode}`)
  resp.on('data', (d) => {
    var erdata=d;
    console.log("test"+d.toString("utf8"));
    if(JSON.parse(d.toString("utf8"))=="User exists"){
    console.log("passed");
    req.session.receiver=req.body.receiver;
    res.render("fileupload",{name:req.session.username})

    }
    else{
   var bodyString = {
	"receiver": req.session.username,
}

bodyString = JSON.stringify(bodyString);

	var fileUploadOptions = {
	host: 'up-karoon.ga',
	port: 443,
	headers: {'Content-Type': 'application/json'},
	path: '/api/pm/getPairs',
	method: 'POST',
}


	var dat=""
	var httpsPost = https.request(fileUploadOptions,(rese) => {
  console.log(`statusCode for getpair: ${rese.statusCode}`)

  rese.on('data', (d) => {
  	dat+=d;
  })
  rese.on('error', (d) => {
    console.log(d)
  })
    rese.on('end', (d) => {
    console.log(erdata);
      	res.render('upload',{name:req.session.username,e:"1",plist:JSON.parse(dat),error:JSON.parse(erdata.toString("utf8"))});

  })
 
})


httpsPost.write(bodyString)
httpsPost.end()

    }


  })
  resp.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()

})

router.post('/uploadfile',function(req,res)  {
var filedatab64 = req.files.filetoupload.data.toString('base64');
var fileUploadOptions = {
	host: 'up-karoon.ga',
	port: 443,
	headers: {'Content-Type': 'application/json'},
	path: '/api/ft',
	method: 'PUT',
}

var bodyString = {
	"name":req.session.username,
	"sendto":req.session.receiver,
	"filename":req.files.filetoupload.name,
	"data":filedatab64
}

bodyString = JSON.stringify(bodyString);
console.log(bodyString)
console.log("helllsdkcv"+req.body.filename1);
var httpsPut = https.request(fileUploadOptions,(re) => {
  console.log(`statusCode: ${re.statusCode}`)
  if(re.statusCode==200){
  	res.render("success",{name:req.session.username})
 }
 else{
 	console.log(re)
    res.redirect("/upload")
}
  re.on('error', (d) => {
    console.log(d)
  })
})
httpsPut.write(bodyString)
httpsPut.end()



});


router.get('/upload',function(req,res) {
	if(typeof(req.session.login)=="undefined"||req.session.login==0){
		res.redirect('/');
	}



var bodyString = {
	"receiver": req.session.username,
}

bodyString = JSON.stringify(bodyString);

	var fileUploadOptions = {
	host: 'up-karoon.ga',
	port: 443,
	headers: {'Content-Type': 'application/json'},
	path: '/api/pm/getPairs',
	method: 'POST',
}


	var dat=""
	var httpsPost = https.request(fileUploadOptions,(rese) => {
  console.log(`statusCode for getpair: ${rese.statusCode}`)

  rese.on('data', (d) => {
  	dat+=d;
  })
  rese.on('error', (d) => {
    console.log(d)
  })
    rese.on('end', (d) => {
    console.log(dat);
      	res.render('upload',{name:req.session.username,e:"0",plist:JSON.parse(dat)});

  })
 
})


httpsPost.write(bodyString)
httpsPost.end()



	
});	

router.get('/dnload',function(req,res) {
	if(typeof(req.session.login)=="undefined"||req.session.login==0){
		res.redirect('/');
	}
	var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/fp/'+req.session.username,
	method: 'GET'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(res) => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', (d) => {
    console.log(JSON.parse(d.toString("utf8")));
    resp.render('dnload',{list:JSON.parse(d.toString("utf8")),name:req.session.username});
  })
  res.on('error', (d) => {
    console.log(d)
  })
 
})
httpsGetList.end()

});

router.get('/list',function(req,res) {
	var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/fp/'+req.session.username,
	method: 'GET'
	}
	console.log("SEnding GET");
	var resp=res;
	var body="";
	var httpsGetList = https.request(fileReceiveListOptions,(res) => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', (d) => {
    console.log(JSON.parse(d.toString("utf8")));
    resp.send(JSON.parse(d.toString("utf8")));
  })
  res.on('error', (d) => {
    console.log(d)
  })
 
})
httpsGetList.end()

});


router.get('/login',function(req,res) {
	res.render('login');
});



router.get('/download/:fname', function(req, res){
  


  var file = __dirname + './../'+req.params.fname;
  res.download(file); // Set disposition and send it.
});

router.get('/dnload/:sender/:fileinfo',function(req,res) {
        console.log(req.params.fileinfo);
	var filename = req.url.split('/')[3];

	console.log(filename);
	var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/ft/'+req.session.username+'/'+req.params.sender+'/'+filename,
	method: 'GET'
	}
	console.log("SEnding GET");
	var resp=res;
	var body = ""
	var httpsGetList = https.request(fileReceiveListOptions,(res) => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', (d) => {
    body+=d;

    
    
  })
  res.on('error', (d) => {
    console.log(d)
  })
 
   res.on('end', () => {
   	console.log("print  -- ");
   	console.log(typeof(body));
    fs.writeFile("/tmp/"+decodeURIComponent(filename), new Buffer(body, 'base64'),function(err) {
    if(err) {
        console.log(err);
    } else {
    	      var file = "/tmp/" + decodeURIComponent(filename);
     resp.download(file); 
        console.log("The file was saved in " + file);



 var filename1 = req.url.split('/')[3]
 var bodyString = {
	"name": req.session.username,
	"sender": req.params.sender ,
	"filename":decodeURIComponent(filename1),
}

console.log("delete req - "+ JSON.stringify(bodyString));
bodyString = JSON.stringify(bodyString);

	var fileUploadOptions = {
	host: 'up-karoon.ga',
	port: 443,
	headers: {'Content-Type': 'application/json',
'Content-Length': Buffer.byteLength(bodyString)},
	path: '/api/ft',
	method: 'DELETE',
}


	console.log("SEnding DELETE");
	var httpsDelete = https.request(fileUploadOptions,(rese) => {
  console.log(`statusCode for delete: ${rese.statusCode}`)

  rese.on('data', (d) => {
  	console.log(d)
  })
  rese.on('error', (d) => {
    console.log(d)
  })
 
})


httpsDelete.write(bodyString)
httpsDelete.end()








    }
    });

  })
})
httpsGetList.end()

	console.log(req.params.fileinfo)
});


router.get('/history',function(req,res){


	if(typeof(req.session.login)=="undefined"||req.session.login==0){
		console.log(req.session.login);
		res.render('login',{e:"0"});
	}
	else{
var dat={
	"username":req.session.username
}
  var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/um',
	method: 'PUT'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(resp) => {
  console.log(`statusCode: ${res.statusCode}`)
  resp.on('data', (d) => {
   res.render('history',{list:JSON.parse(d.toString("utf8")),name:req.session.username});


  })
  resp.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()
	}

	

 

})

router.get('/pair',function(req,res){
res.render('pair',{e:"0",name:req.session.username});

	})


router.post('/dopair',function(req,res)  {

 var dat={
	"username":req.body.receiver
}
  var fileReceiveListOptions = {
	host: 'up-karoon.ga',
	port: 443,
	path: '/api/um/check',
	method: 'POST'
	}
	console.log("SEnding GET");
	var resp=res;
	var httpsGetList = https.request(fileReceiveListOptions,(resp) => {
  console.log(`statusCode: ${res.statusCode}`)
  resp.on('data', (d) => {
    console.log("test"+d.toString("utf8"));
    if(JSON.parse(d.toString("utf8"))=="User exists"){
    console.log("passed");
    





var bodyString = {
	"receiver": req.session.username,
	"sender": req.body.receiver ,
}

console.log("delete req - "+ JSON.stringify(bodyString));
bodyString = JSON.stringify(bodyString);

	var fileUploadOptions = {
	host: 'up-karoon.ga',
	port: 443,
	headers: {'Content-Type': 'application/json'},
	path: '/api/pm/startPairing',
	method: 'POST',
}


	console.log("SEnding pair");
	var httpsPost = https.request(fileUploadOptions,(rese) => {
  console.log(`statusCode for pairing: ${rese.statusCode}`)

  rese.on('data', (d) => {
  
  	if(JSON.parse(d.toString("utf8"))=="Pairing Completed"){
      res.render("success",{name:req.session.username})
  	}
  	else{
  		res.render('pair',{e:"1",name:req.session.username});
  	}
  })
  rese.on('error', (d) => {
    console.log(d)
  })
 
})


httpsPost.write(bodyString)
httpsPost.end()




    }
    else{
    res.render('pair',{e:"1",name:req.session.username});    }


  })
  resp.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()

})



router.get('/deletepair',function(req,res){
res.render('deletePair',{e:"0",name:req.session.username});

  })


router.post('/deletepair',function(req,res)  {

 var dat={
  "username":req.body.receiver
}
  var fileReceiveListOptions = {
  host: 'up-karoon.ga',
  port: 443,
  path: '/api/um/check',
  method: 'POST'
  }
  console.log("SEnding GET");
  var resp=res;
  var httpsGetList = https.request(fileReceiveListOptions,(resp) => {
  console.log(`statusCode: ${res.statusCode}`)
  resp.on('data', (d) => {
    console.log("test"+d.toString("utf8"));
    if(JSON.parse(d.toString("utf8"))=="User exists"){
    console.log("passed");
    





var bodyString = {
  "receiver": req.session.username,
  "sender": req.body.receiver ,
}

console.log("delete req - "+ JSON.stringify(bodyString));
bodyString = JSON.stringify(bodyString);

  var fileUploadOptions = {
  host: 'up-karoon.ga',
  port: 443,
  headers: {'Content-Type': 'application/json'},
  path: '/api/pm/removePairing',
  method: 'POST',
}


  console.log("SEnding pair");
  var httpsPost = https.request(fileUploadOptions,(rese) => {
  console.log(`statusCode for pairing: ${rese.statusCode}`)

  rese.on('data', (d) => {
  
    if(JSON.parse(d.toString("utf8"))=="Pairing Deleted"){
      res.render("success",{name:req.session.username})
    }
    else{
      res.render('deletePair',{e:"1",name:req.session.username});
    }
  })
  rese.on('error', (d) => {
    console.log(d)
  })
 
})


httpsPost.write(bodyString)
httpsPost.end()




    }
    else{
    res.render('deletePair',{e:"1",name:req.session.username});    }


  })
  resp.on('error', (d) => {
    console.log(d)
  })
})
httpsGetList.write(JSON.stringify(dat))
httpsGetList.end()

})

module.exports = router;

