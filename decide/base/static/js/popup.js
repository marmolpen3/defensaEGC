	


	function popupMostrar(){
		if(document.getElementById("btn-abrir-popup")!=null){
			var btnAbrirPopup = document.getElementById("btn-abrir-popup");
			var overlay = document.getElementById("overlay");
			var popupadmin = document.getElementById("popupadmin");
			overlay.classList.add("active");
			popupadmin.classList.add("active");
		}
		
	}

	function popQuitar(){
		if(document.getElementById("btn-cerrar-popup")!= null){
			var btnCerrarPopup = document.getElementById("btn-cerrar-popup");
			var overlay = document.getElementById("overlay");
			var popupadmin = document.getElementById("popupadmin");
			overlay.classList.remove("active");
			popupadmin.classList.remove("active");
			
		}
	}
	

	
	

