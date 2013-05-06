$.ajaxSetup({
    async: false 
});
var machine_info=null;
$("input.input-small").keyup(machine_filter);
$("input#host").keyup(machine_filter);
$("#id_machine_get").click(function()
			   {
			       //set button 
			       $("#id_machine_get").attr("class"," retweet  btn btn-danger");
			       $("#id_machine_get").attr("disabled","disabled");
			       $("#icon_button").attr("class","icon-retweet");
			       $("#id_machine_get").text("going");
			       mdict=eval(machine_info)[0]
			       xmlhttp=xmlhttp_create()
			       host_ip=JSON.stringify(mdict)
			       if (xmlhttp==null) return;
			       xmlhttp.onreadystatechange=function()
			       {
				   if (xmlhttp.readyState==4 && xmlhttp.status==200)
				   {
				       $(".deploy-msg").text(xmlhttp.responseText)
				       $('#myModal').modal('hide')
				       
				       
				   }    
			       }
			       var url="/deploynew?machine="+host_ip;
			       url=url+"&sid="+Math.random();
			       xmlhttp.open("GET",url,true);
			       xmlhttp.send(null);

			       
			   }
			  );

function xmlhttp_create(){
    try
    {// Firefox, Opera 8.0+, Safari, IE7
	xmlhttp=new XMLHttpRequest();
	return xmlhttp;
    }
    catch(e)
    {// Old IE
	try
	{
	    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
	    return xmlhttp;
	}
	catch(e)
	{
	    alert ("Your browser does not support XMLHTTP!");
	    return null;  
	}
    }
}
function askserver(){
    var host = $("#host").val();
    var ip = [$("#ip1").val(),$("#ip2").val(),$("#ip3").val(),$("#ip4").val()].join(".");
    var host_ip = {};
    host_ip[host]=ip;
    host_ip=JSON.stringify(host_ip)
    var xmlhttp=xmlhttp_create()
    if (xmlhttp==null) return;
    xmlhttp.onreadystatechange=function()
    {
	if (xmlhttp.readyState==4 && xmlhttp.status==200)
	{
	    machine_info=xmlhttp.responseText
	}    
    }
    var url="/checkmachine?machine="+host_ip;
    url=url+"&sid="+Math.random();
    xmlhttp.open("GET",url,false);
    xmlhttp.send(null);
    
}

function machine_filter(){

    // buttion diabled 
    $("#id_machine_get").attr("class","btn btn-inverse");
    $("#id_machine_get").attr("disabled","disabled");
    //check the host
    if ( $("#host").val().length!=0){
	$("#right1").attr("class","icon-ok");
	$(".error-msg1").text("");
    }
    else{
	$(".error-msg1").text("host不能为空");
	$("#right1").attr("class","");
    }
    //check the ip
    var ip=[];
    $("input.input-small").each(function(){ip.push($(this).val())});
    var right=0;
    for(var i=0; i<4;i++)
    {
	num_i=parseInt(ip[i]);
	if(num_i>=0&&num_i<=255 &&num_i==ip[i]){
	    $("#ip"+(i+1)).css("border","1px solid green");
	    right=right+1;
	}
	else{
	    $("#ip"+(i+1)).css("border","1px solid red");
	    $(".error-msg2").text("输入不合法");
	    $("#right2").attr("class","");

	}
    }
    if (right==4){
	$(".error-msg1").text("");
	$(".error-msg2").text("");
	askserver();
	console.log(machine_info);
	info=eval(machine_info)
	if( info[0]=="0"){
	    $("#right1").attr("class","");
	    $(".error-msg1").text(info[1]);
	}
	if(info[0]=="1"){
	    $("#right2").attr("class","");
	    $(".error-msg2").text(info[1]);
	}
	if (info[0]!=="0" && info[0]!=="1"){
	    $("#right1").attr("class","icon-ok");
	    $("#right2").attr("class","icon-ok");
	    $("#id_machine_get").attr("class","btn btn-success");
	    $("#id_machine_get").removeAttr("disabled");

	}

	
    }
}


function send(obj){
    
    var id=parseInt(obj.id)
    var host=$("table tr:eq("+obj.id+") td:eq(0)").text();
    var ip=$("table tr:eq("+obj.id+") td:eq(1)").text();
    var host_ip=JSON.stringify({host:ip});
    $.get("/start?machine="+host_ip+"&sid="+Math.random(),function(data,status){

	if( status=="success"){
	    if( data=="success"){
		$("button#"+id+" i").attr("class","icon-pause");
		$("button#"+id).attr("class","btn btn-warning");
	    }
	    
	}
	else
	    alert("send obj failed");
	
    });
}

function show(ip) {

    Highcharts.setOptions({
	global : {
	    useUTC : false
	}
    });
    
    // Create the chart
    $('#container1').highcharts('StockChart', {
	chart : {
	    events : {
		load : function() {

		    // set up the updating of the chart each second

		    var series = this.series[0];

		    setInterval(function() {
			var x = (new Date()).getTime(), // current time
			y=function(){		   
			    var info;
			    $.get("/get_info?ip="+ip+"&sid="+Math.random(),function(data,status){

				if (data!="None"){
				    data=eval(data);
				    info=eval(data[0]);
				}
				else
				    info=0;
			    });
			    return info;
			    
			} ();

			series.addPoint([x, y], true, true);
		    },2000);

		}
	    }
	},
	
	rangeSelector: {
	    buttons: [{
		count: 1,
		type: 'minute',
		text: '1M'
	    }, {
		count: 5,
		type: 'minute',
		text: '5M'
	    }, {
		type: 'all',
		text: 'All'
	    }],
	    inputEnabled: false,
	    selected: 0
	},
	
	title : {
	    text : 'cpu使用率'
	},
	
	exporting: {
	    enabled: false
	},
	
	series : [{
	    name : '%',
	    data : (function() {
		// generate an array of random data

		time = (new Date()).getTime();
		var data=[];var datas;
		$.get("/init_info?ip="+ip,function(data,status){
		    datas=eval(data);
		});
		var n=0,info,len=datas.length;
		for( i = -1*len; i <0; i++){
		    info=eval(eval(datas[n])[0]);
		    if (n>=len) break;
		    data.push([
			time+i*2000,
			info
		    ]);
		    n=n+1;
		}
		return data;

	    })()
	}]
    });
    $('#container2').highcharts('StockChart', {
	chart : {
	    events : {
		load : function() {

		    // set up the updating of the chart each second

		    var series = this.series[0];

		    setInterval(function() {
			var x = (new Date()).getTime(), // current time
			y=function(){		   
			    var info;
			    $.get("/get_info?ip="+ip+"&sid="+Math.random(),function(data,status){

				if (data!="None"){
				    data=eval(data);
				    info=eval(data[1]);
				}
				else
				    info=0;
			    });
			    return info;
			    
			} ();

			series.addPoint([x, y], true, true);
		    },2000);

		}
	    }
	},
	
	rangeSelector: {
	    buttons: [{
		count: 1,
		type: 'minute',
		text: '1M'
	    }, {
		count: 5,
		type: 'minute',
		text: '5M'
	    }, {
		type: 'all',
		text: 'All'
	    }],
	    inputEnabled: false,
	    selected: 0
	},
	
	title : {
	    text : '内存使用率'
	},
	
	exporting: {
	    enabled: false
	},
	
	series : [{
	    name : '%',
	    data : (function() {
		// generate an array of random data

		time = (new Date()).getTime();
		var data=[];var datas;
		$.get("/init_info?ip="+ip,function(data,status){
		    datas=eval(data);
		});
		var n=0,info,len=datas.length;
		for( i = -1*len; i <0; i++){
		    info=eval(eval(datas[n])[1]);
		    if (n>=len) break;
		    data.push([
			time+i*2000,
			info
		    ]);
		    n=n+1;
		}
		return data;

	    })()
	}]
    });

    $('#container3').highcharts('StockChart', {
	chart : {
	    events : {
		load : function() {
		    // set up the updating of the chart each second
		    var series1 = this.series[0];
		    var series2 = this.series[1];
		    setInterval(function() {
			var x = (new Date()).getTime(), // current time
			y=function(){		   
			    var info;
			    $.get("/get_info?ip="+ip+"&sid="+Math.random(),function(data,status){
				if (data!="None"){
				    data=eval(data);
				    info1=eval(eval(data[2])[0]);
				    info2=eval(eval(data[2])[1]);

				}
				else{
				    info1=0;
				    info2=0;
				    }
				
			    });
			    return [info1,info2];
			    
			} ();
			
			series1.addPoint([x, y[0]], true, true);
			series2.addPoint([x, y[1]], true, true);
		    },2000);

		}
	    }
	},
	
	rangeSelector: {
	    buttons: [{
		count: 1,
		type: 'minute',
		text: '1M'
	    }, {
		count: 5,
		type: 'minute',
		text: '5M'
	    }, {
		type: 'all',
		text: 'All'
	    }],
	    inputEnabled: false,
	    selected: 0
	},
	
	title : {
	    text : '网络使用情况'
	},
	
	exporting: {
	    enabled: false
	},
	
	series : [{
	    name : 'recive kb/s',
	    data : (function() {
		// generate an array of random data

		time = (new Date()).getTime();
		var data=[];var datas;
		$.get("/init_info?ip="+ip,function(data,status){
		    datas=eval(data);
		});
		var n=0,info,len=datas.length;
		for( i = -1*len; i <0; i++){
		    info=eval(eval(eval(datas[n])[2])[0]);
		    if (n>=len) break;
		    data.push([
			time+i*2000,
			info
		    ]);
		    n=n+1;
		}
		return data;

	    })()
	},{
	    name : 'send kb/s',
	    data : (function() {
		// generate an array of random data

		time = (new Date()).getTime();
		var data=[];var datas;
		$.get("/init_info?ip="+ip,function(data,status){
		    datas=eval(data);
		});
		var n=0,info,len=datas.length;
		for( i = -1*len; i <0; i++){
		    info=eval(eval(eval(datas[n])[2])[1]);
		    if (n>=len) break;
		    data.push([
			time+i*2000,
			info
		    ]);
		    n=n+1;
		}
		return data;

	    })()
	}]
    });
}
