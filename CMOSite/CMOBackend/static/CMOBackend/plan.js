form_count = 0

function addAction() {
  var li=$('<li>');
  li.attr('id','action'+ form_count);

  new_action_troopType= $('<input type="text"/>');
  new_action_troopType.attr('name', 'extra_action' + form_count + 'troopType');
  new_action_troopType.attr('id', 'extra_action' + form_count + 'troopType');
  var newlabel = document.createElement("Label");
  newlabel.setAttribute("for",'extra_action' + form_count + 'troopType');
  newlabel.innerHTML = "Type of Troop";

  new_action_severity= $('<input type="text"/>');
  new_action_severity.attr('name', 'extra_action_' + form_count + 'severity');
  var newlabel2 = document.createElement("Label");
  newlabel2.setAttribute("for",'extra_action' + form_count + 'severity');
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
