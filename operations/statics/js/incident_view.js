incident = {}

incident.incident_document_delete = function(url) {
    $("#incident_document_delete_modal a.btn").attr("href", url);
}

$(function() {

    $("#id_vehicle, #id_driver, #id_division, #id_incident_date, #id_cost, #id_description").prop('disabled', true);
    $("#id_reference_number, #id_incident_type, #id_documents-document, #id_documents-document_type").prop('disabled', true);
    $('label[for="id_reason_other"]').hide()

});