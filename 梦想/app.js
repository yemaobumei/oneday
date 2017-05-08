var settings={
	operation: "POST",
	headers:{
		'Host': 'app0.dreamlive.tv',
		'Accept': '*/*',
		'Connection': 'keep-alive',
		'app_ct': 'CN',
		'app_v': '2.0.9',
		'Accept-Encoding': 'gzip, deflate',
		'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
		'Content-Type': 'application/x-www-form-urlencoded',
		'Content-Length': '163',
		'User-Agent': 'Dreamer/2.0.9 (iPhone; iOS 10.1.1; Scale/2.00)',
		'Connection': 'keep-alive',
		'app_type': '0',
		'Cookie': 'JSESSIONID=F9F975F8153A46BEAC2BB0F70CAE3B0E',
		'app_dev': '5C8448A1-1D70-4541-A9D3-37187C1382CA'
	},
	data:'account=13126772351&deviceId=5C8448A1-1D70-4541-A9D3-37187C1382CA&mcheck=85a2f3692ca36aa3cde735d911c4c99c&password=9ef1969d6ed8fc9a289ef6b0e48e13b6&r='+(new Date()).getTime()
	// data:JSON.stringify({
	// 	'account':'13126772351',
	// 	'deviceId':'5C8448A1-1D70-4541-A9D3-37187C1382CA',
	// 	'mcheck':'85a2f3692ca36aa3cde735d911c4c99c',
	// 	'password':'9ef1969d6ed8fc9a289ef6b0e48e13b6',
	// 	'r':'1484566983751'
	// })
}
var url='http://app0.dreamlive.tv/passport/login/AccountLoginAction.a'
var webPage = require('webpage');
var page = webPage.create();
page.open(url, settings,function (s) {
		console.log(s);
	});