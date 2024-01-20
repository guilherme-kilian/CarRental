const VehiclesTable = {

    colorClass: '.car-color',

    getSpanColor(vehicleId){
      return $(`span[name=color-${vehicleId}]`)
    },

    getSpanYear(vehicleId){
      return $(`span[name=year-${vehicleId}]`)
    },

    init(){
      VehiclesTable.initalizeVehicle();
    },

    initalizeVehicle(){

      let colors = $(VehiclesTable.colorClass)

      colors.each(c => {
        const input = colors[c]
        const vehicleId = input.dataset.vehicle

        $.get(`/vehicles/${vehicleId}`, function(res){
          VehiclesTable.getSpanColor(vehicleId).text(res.color)          
          VehiclesTable.getSpanYear(vehicleId).text(res.year)
        }).fail(function(error) {
          alert('erro ao carregar tabela')
        })
      })
    },
}

const DownloadButton = {
  init(){
    $('#report-download').on('click', DownloadButton.download)
  },

  download(e){

    body = $('#report-div').children().first().html()

    $.ajax({
      type: "POST",
      url: "/rentals/download",
      data: body,
      contentType: "text/html",
      success: function(response) {
        if(response.fileUrl){
          window.location.href = response.fileUrl
        }
      },
      error: function(error) {
        console.log("Erro ao realizar download");
      }
    });
  },
}

$(function() {
  VehiclesTable.init()
  DownloadButton.init()
});