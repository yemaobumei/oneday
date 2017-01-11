var settings={
	operation: "GET",
	headers:{
			'Host': 'h5.weiyingonline.com',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Connection': 'keep-alive',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_1_1 like Mac OS X) AppleWebKit/602.2.14 (KHTML, like Gecko) Mobile/14B100 MicroMessenger/6.5.3 NetType/WIFI Language/zh_CN',
			'Accept-Language': 'zh-cn',
			'Accept-Encoding': 'gzip, deflate',
			'Connection': 'keep-alive',
		}
}


//循环访问直播网页	
var i=0;
//var phantom = require('phantom');
var webPage = require('webpage');
var page = webPage.create();
var url='http://h5.weiyingonline.com/share_play/SharePlayClickAction.a?shareDetailId=1181862'
function iter(){
	var page=null;
	page = webPage.create();
	page.open(url, settings,function (s) {
	  console.log(s);
	var cookies = page.cookies;
	console.log(cookies[0].name+":"+cookies[0].value);
	console.log(cookies[1].name+":"+cookies[1].value);
	phantom.exit();
	});
	
	//setTimeout(arguments.callee, 3000)
}
iter()