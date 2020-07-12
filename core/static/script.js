


var initialCoordinates = [-5.11, -42.75]; // Rio de Janeiro
var initialZoomLevel = 12;
var funcionarios;

var atualizarAutomaticamente = false;



// create a map in the "map" div, set the view to a given place and zoom
var map = L.map('map').setView(initialCoordinates, initialZoomLevel);






function getMarkers(planes) {
  map.remove();
  map = L.map('map').setView(initialCoordinates, initialZoomLevel);

// add an OpenStreetMap tile layer
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; Contribuidores do <a href="http://osm.org/copyright">OpenStreetMap</a>'
}).addTo(map);
    for (var i = 0; i < planes.length; i++) {

      marker = new L.marker([planes[i][1],planes[i][2]]).bindPopup(planes[i][0]).addTo(map);
    }
  }



$('#atualizar').change(function() {
        if(this.checked) {
            atualizarAutomaticamente = true;
        }else{
            atualizarAutomaticamente = false;
        }

    });


$.ajax({
                    type : 'POST',
					url : '/api/empresas',
					success : function(data) {

					//primeiro input de cargos
						var element = document.getElementById('name_input1');
						element.innerHTML = '<b>Empresas</b>';

						for(i = 0; i< data.length; i++){
						    var x = document.createElement('option');
						        x.setAttribute('value', data[i].id);
					            var t = document.createTextNode(data[i].nome);
					            x.appendChild(t);
					            document.getElementById('select1').appendChild(x);
						}

						selectFuncionario('0');

					}
				});

function selectFuncionario(id){

$.ajax({
									type : 'POST',
									contentType : 'application/json',
									url : '/api/funcionarios',
									data : JSON.stringify(id),
									dataType : 'json',
									success : function(data) {
									funcionarios = data;

									//primeiro input de cargos
						var element = document.getElementById('name_input2');
						element.innerHTML = '<b>Funcionarios</b>';

						$('#select2').children().remove();

						for(i = 0; i< data.length; i++){
						    var x = document.createElement('option');
						        x.setAttribute('value', data[i].id);
					            var t = document.createTextNode(data[i].nome);
					            x.appendChild(t);
					            document.getElementById('select2').appendChild(x);
						}


						var planes = [];


                        for(i = 1; i < data.length; i ++){
                        var object = [data[i].nome, data[i].latitude, data[i].longitude];
                        planes.push(object);
                        }
                        console.log(planes.length);
                        getMarkers(planes);

									}
									});

}



function threadAtualiza(){
    if(atualizarAutomaticamente == false){
        setTimeout(threadAtualiza, 2000);
        console.log('sair');
        return;
    }
    var value = $('#select2').val();
    console.log('>>>> INICIO DA THREAD');

    if(value != 0){
                        var planes = [];


                        for(i = 1; i < funcionarios.length; i ++){
                        if(funcionarios[i].id == value){
                        var object = [funcionarios[i].nome, funcionarios[i].latitude, funcionarios[i].longitude];
                        planes.push(object);
                        }

                        }

                        getMarkers(planes);

}else{
                        var planes = [];


                        for(i = 1; i < funcionarios.length; i ++){

                        var object = [funcionarios[i].nome, funcionarios[i].latitude, funcionarios[i].longitude];
                        planes.push(object);


                        }

                        getMarkers(planes);


}


    setTimeout(threadAtualiza, 2000);
}

setTimeout(threadAtualiza, 2000);


$('#select1').on('change', function() {

selectFuncionario(this.value);

});


$('#select2').on('change', function() {

if(this.value != 0){
var planes = [];


                        for(i = 1; i < funcionarios.length; i ++){
                        if(funcionarios[i].id == this.value){
                        var object = [funcionarios[i].nome, funcionarios[i].latitude, funcionarios[i].longitude];
                        planes.push(object);
                        }

                        }

                        getMarkers(planes);

}else{
var planes = [];


                        for(i = 1; i < funcionarios.length; i ++){

                        var object = [funcionarios[i].nome, funcionarios[i].latitude, funcionarios[i].longitude];
                        planes.push(object);


                        }

                        getMarkers(planes);


}


});


