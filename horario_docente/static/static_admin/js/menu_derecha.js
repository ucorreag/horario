$('document').ready(function(){
       $('#newprofessor').click(function(){ 
		$('#crearprofesor h4').text('Crear Profesor');				
		$('#crearprofesor #nombreprofesor').attr('value','');
		$('#crearprofesor #titulo').attr('value','');
		$('#crearprofesor #crearp').attr('value','Crear');				
		$('#formcrearpro').attr('action','/administracion/crear_profesor/');
			          
       $('#crearprofesor').modal('show');
       });
       
        $('#newadmin').click(function(){   
		$('#crearplanificador h4').text('Crear Planificador');
				
		$('#crearplanificador #nombres').attr('value','');
		$('#crearplanificador #apellidos').attr('value','');
		$('#crearplanificador #usuarios').attr('value','');
		$('#crearplanificador #emails').attr('value','');
		$('#crearplanificador #creando').attr('value','Crear');
		$('#formcreandopl').attr('action','/administracion/crear_usuario/');
			   	    
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
                      $('#administra').append("<li><a class=\"item\">"+objeto.usuario+" ("+objeto.nombre+" "+objeto.apellido+")<span onclick=\"eliminarplanificador(this);\" class=\"mif-minus fg-white eliminandoall\" name=\"" + objeto.usuario +
                        "-" + objeto.id + "\"></span><span class=\"mif-sync-problem actualizandoall\" onclick=\"actualizarplanificador(this);\" name=\""+objeto.id+"\"></span></a><div>"+
						"<h5>Nombre = "+objeto.nombre+"</h5>"+
						"<h5>Apellidos = "+objeto.apellido+"</h5>"+
						"<h5>Usuario = "+objeto.usuario+"</h5>"+
						"<h5>E-Mail = "+objeto.email+"</h5>"						
						
						+"</div></li>"); 
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
                      $('#profesores').append("<li><a class=\"item\">"+objeto.nombre+" ("+objeto.titulo+") <span onclick=\"eliminarprof(this);\" class=\"mif-minus fg-white eliminandoall\" name=\"" + objeto.nombre +
                        "-" + objeto.id + "\"></span><span class=\"mif-sync-problem actualizandoall\" onclick=\"actualizarprofesor(this);\" name=\""+objeto.id+"\"></span></a><div>"+
						"<h5>Nombre = "+objeto.nombre+"</h5>"+
						"<h5>Titulo = "+objeto.titulo+"</h5>"											
						
						+"</div></li>"); 
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
  
  //actualizar planificador
   function actualizarplanificador(e){	
		var aux=$(e).attr('name');
		$.ajax({
			url:'/administracion/data_user_update/',
		    type:'GET',						
			data:{'id':aux},
			success: function(data){
				$('#crearplanificador h4').text('Actualizar Planificador');
				
				$('#crearplanificador #nombres').attr('value',data.nombre);
				$('#crearplanificador #apellidos').attr('value',data.apellidos);
				$('#crearplanificador #usuarios').attr('value',data.usuario);
				$('#crearplanificador #emails').attr('value',data.email);
			    $('#crearplanificador #creando').attr('value','Actualizar');
			    $('#formcreandopl').attr('action','/administracion/actualizar_planificador/'+aux+'/');
			    				
				$('#crearplanificador').modal('show');
				
			},
			 error: function(err){
				alert('error'+err.error);
			},			
			
			
		});
			
				
  };
  
    function actualizarprofesor(e){	
		var aux=$(e).attr('name');
		$.ajax({
			url:'/administracion/data_profesor/',
		    type:'GET',						
			data:{'id':aux},
			success: function(data){
				$('#crearprofesor h4').text('Actualizar Profesor');
				
				$('#crearprofesor #nombreprofesor').attr('value',data.nombre);
				$('#crearprofesor #titulo').attr('value',data.titulo);
				$('#crearprofesor #crearp').attr('value','Actualizar');
				
				$('#formcrearpro').attr('action','/administracion/actualizar_profesor/'+aux+'/');
			    				
				$('#crearprofesor').modal('show');
				
			},
			 error: function(err){
				alert('error'+err.error);
			},			
			
			
		});
			
				
  };
  
  
 