
$(document).ready(function() {
    $('#id_existing_event').change(function(e) {
        $('#id_new_name').val($('option:selected', this).text());
    });
});