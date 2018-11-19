

  $.ajax({
    url: '/list',
    type: 'GET',
    contentType: "application/json",
    success: function(data) {
       // console.log('form submitted.' + data);
    }
  });

  function myFunction(s){
    console.log(s);
    $.ajax({
    url: '/dnload/'+s,
    type: 'GET',
    contentType: "application/json",
    success: function(data) {
        console.log(data);
         var element = document.createElement('a');
    element.setAttribute('href', 'data:application/png;charset=utf-8,' + encodeURIComponent(data));
    element.setAttribute('download', s.split("/")[1]);

    element.style.display = 'none';
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
    }
  });
  }
