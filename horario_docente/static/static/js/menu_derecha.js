$('document').ready(function(){
       $('#newprofessor').click(function(){       
       $('#crearprofesor').modal('show');
       });
       
        $('#newadmin').click(function(){       
       $('#crearplanificador').modal('show');
       });
       
       //verificar contraseña
       $('#repas').keyup(function(){  
         var $pass = $('#pas').val();
         var $repass = $('#repas').val();      
         if($pass!=$repass){            
         $('#message-pass-error1').attr('style','visibility: visible; color:red;'); 
         }else{
         $('#message-pass-error1').attr('style','visibility: hidden;'); 
         }
         });
       
       //planificadores
       $.ajax({
				 url:'/administracion/lista_usuarios/',
				 type:'GET',						
				 data:null,
				 success: function(data){
                    
                    $.each(data, function(index, objeto){
                      $('#administra').append("<li><a href=\"#\" class=\"item\">"+objeto.usuario+" ("+objeto.nombre+")<span onclick=\"eliminarplanificador(this);\" class=\"mif-minus fg-white eliminandoall\" name=\"" + objeto.usuario +
                        "-" + objeto.id + "\"></span></a></li>"); 
                    });                        
                     
                     
                 },
                 error: function(err){
								alert('error'+err.error);
			},
       });
       
       
       
       //profesores
        $.ajax({
				 url:'/administracion/lista_profesores/',
				 type:'GET',						
				 data:null,
				 success: function(data){
                    
                    $.each(data, function(index, objeto){
                      $('#profesores').append("<li><a href=\"#\"class=\"item\">"+objeto.nombre+" ("+objeto.titulo+") <span onclick=\"eliminarprof(this);\" class=\"mif-minus fg-white eliminandoall\" name=\"" + objeto.nombre +
                        "-" + objeto.id + "\"></span></a></li>"); 
                      $('#profesorrr').append("<option value=\""+objeto.id+"\">"+objeto.nombre+" ("+objeto.titulo+")</option>");						  
								
                    });                        
                     
                     
                 },
                 error: function(err){
								alert('error'+err.error);
			},
       });
       
      
      
      var contador=1;
		$('#activar-derecha').click(function(){
			if (contador==1){
				$('.menu_derecha').animate({
					right:'0'
				});
				
				contador=0;
			
			}else{
				$('.menu_derecha').animate({
					right:'-350px'
				});
				
				contador=1;
			}
		});
		
      

	$('.der').click(function(){
		$(this).children('ul').slideToggle();
	});
	$('.menu_derecha ul').click(function(e){
		e.stopPropagation();
	});
  $('.nuevoo').click(function(e){
		e.stopPropagation();
	});
   
	
});

 function eliminarasigna(e){	
		var aux=$(e).attr('name').split('-');
    
		$('#textoeliminarasignatura').text('¿Desea eliminar la asignatura '+ aux[0] + '?');
				
		$('#formularioeliminarasignatura').attr('action','/administracion/eliminar_asignatura/'+aux[1]+'/');
		$('#modalea').modal('show');		
				
  };

  function eliminarprof(e){	
		var aux=$(e).attr('name').split('-');
    
		$('#textoeliminarasignatura').text('¿Desea eliminar el profesor '+ aux[0] + '?');
				
		$('#formularioeliminarasignatura').attr('action','/administracion/eliminar_profesor/'+aux[1]+'/');
		$('#modalea').modal('show');		
				
  };
  
 