form_count = $( "li" ).length + 1;
$("[name=total_input_fields]").val(form_count);
troop_choices = {
  'MIL' : 'Military',
  'BDP' : 'Bomb Disposal',
  'CGD' : 'Coast Guard',
  'HAZ' : 'Hazmat',
  'SNR' : 'Search and Rescue',
  'CEV' : 'Civilian Evacuation',
  'AMB' : 'Ambulance',
  'ETC' : 'Emergency Traffic Control',
  'FFT' : 'Firefighters',
  'IDQ' : 'Infectious Disease Quarantine Personnel'
};

$.ajax({url: "https://maps.googleapis.com/maps/api/geocode/json?address="+$('#location').val()+"&key="+'AIzaSyAxmNbmdGzDgu_sdi7Je0ENXOmDm80P7wU', success: function(result){
  $('#lat').val(result.results[0].geometry.location.lat)
  $('#lng').val(result.results[0].geometry.location.lng)
  }});

function addAction() {
  var li=$('<li></li>');
  li.attr('id','action'+ form_count);

  new_action_troopType= $('<select></select>');
  new_action_troopType.attr('name', 'action' + form_count + 'troopType');
  for (choice in troop_choices){
    troopType_option= $('<option value="'+choice+'">'+troop_choices[choice]+'</option>');
    new_action_troopType.append(troopType_option);
  }
  var newlabel = document.createElement("Label");
  newlabel.setAttribute("for",'action' + form_count + 'troopType');
  newlabel.innerHTML = "Type of Troop";

  new_action_severity= $('<select></select>');
  new_action_severity.attr('name', 'action' + form_count + 'severity');
  for (var i =1; i<=5; i++){
    severity_option= $('<option value="'+i+'">'+i+'</option>');
    new_action_severity.append(severity_option);
  }
  var newlabel2 = document.createElement("Label");
  newlabel2.setAttribute("for",'action' + form_count + 'severity');
  newlabel2.innerHTML = "Severity Level";

  var removeButton = document.createElement('button');
  removeButton.setAttribute('onclick','removeAction("'+'action'+ form_count+'")');
  removeButton.setAttribute('type','button');
  removeButton.innerHTML = '&#10006;'

  li.append(newlabel);
  li.append(new_action_troopType);
  li.append(newlabel2);
  li.append(new_action_severity);
  li.append(removeButton);
  // append the new element in your html
  $("#suggested_actions").append(li);
  // increment the form_count variable
  form_count ++;
  // save the form_count to another input element (you can set this to invisible. This is what you will pass to the form in order to create the django form fields
  $("[name=total_input_fields]").val(form_count);
}

function removeAction(li_id) {
  $("#"+li_id).remove();
}
