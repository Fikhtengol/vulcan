window.onload = function change(){
        var template_name = window.location.href.split('/')[3];
        index = template_name.indexOf('?');
        if (index>0)
            template_name = template_name.substring(0 , index);
        var li_item = document.getElementById(template_name);
        li_item.className = "active";
    };
$(document).ready(
function(){
	$(".update_position").click(
		function(event){
		  if (this.name == "btn_update_position") {
			  tab = document.getElementById("scripts_table").getElementsByTagName("input");
			  var s = "";
			  var sort_list ;
			  for (var i = 0, len	= tab.length ; i< len ;i++) {
				  if(tab[i].type == "hidden") {
					  if ( tab[i].name == "select_script_id" ){
						  s += tab[i].value; s += "|";
					  }
					  else if (tab[i].name == "sort_list"){
						  sort_list = tab[i]
					  }
				  }
			  }
			  sort_list.value = s;
		  }
		}
	);
});


