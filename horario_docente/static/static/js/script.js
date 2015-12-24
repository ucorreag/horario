
$('document').ready(carreras);

function carreras(){
	$('a.carrera').each(
		function(){
		var texto= $(this).attr('name');
		var valor= $(this);
		$.ajax({
				 url:'/administracion/issemana/',
				 type:'GET',						
				 data:{'id':texto},
				 success: function(data){
							 
				 if (data.semana){				    
				   valor.attr('href',"/administracion/crear_horario/"+texto+"");
					
				}
				}
		
		   });
	});
 }

				 