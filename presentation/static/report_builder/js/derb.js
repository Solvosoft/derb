/**
 * Created by jaquer on 09/08/16.
 */

/**
 * Variables
 */
var max_message_queue = 3;
var last_type = '';
var otables = {};

function randomInt(min, max) {
    return Math.floor(Math.random() * (max - (min + 1)) + (min + 1));
}

function _alert(type, message, append) {
    var queue = $('#message_queue');
    var children = queue.children();
    var max_length = children.length;
    if (max_length == 0) {
        append = undefined
    }
    if (append != undefined && last_type != type) {
        append = undefined;
        last_type = type;
    }
    if (append == undefined) {
        if (max_length > max_message_queue) {
            $(queue.children()[0]).remove();
            max_length -= 1;
        }
        var li_id = "li_" + randomInt(1000, 10000);
        var m = '<li id="' + li_id + '"><div class="alert ' + type + ' alert-dismissable">' +
            '<button type="button" class="close" data-dismiss="alert" aria-hidden="true" onclick="delete_alert(this)">&times;</button>' +
            '<div class="alert_body">' + message + '</div></div></li>';

        queue.append(m);
        setTimeout("clean_queue('#" + lid + "')", 15000);
    } else {
        $(children[max_length - 1]).find('.alert_body').append('<br>' + message);
    }
}

function delete_alert(self) {
    $(self).closest('li').remove();
}

function clean_queue(id) {
    var queue = $('$message_queue');
    queue.find(id).remove();
}

function django_ajax_alert(response) {
    if (response.status == 0) {
        _alert('alert-danger', 'No response from the server. Generally this error is temporary, please try again in a few minutes');
    } else {
        _alert('alert-danger', 'Temporary error: ' + response.status + ' ' + response.statusText + ' ' + response.content);
    }
}

function save_form(question_id, async, display_alert) {
    if (async == undefined) async = true;
    if (display_alert == undefined) display_alert = true;

    var form = $($('#' + question_id).find('form')[0]);
    try {
        load_subquestions(form, question_id);
    } catch (error) {
        return 1;
    }

    var question = get_question_from_pool(question_id);
    var url = form.attr('action');
    if (question_pool[question].pk != -1) {
        url += question_pool[question].pk
    }

    $.ajax({
        type: 'POST',
        async: async,
        url: url,
        data: form.serialize(),
        error: function (jqXHR, textStatus, errorThrown) {
            django_ajax_alert(jqXHR);
        },
        success: function (data) {
            if ($.isNumeric(data)) {
                if (question_pool[question].pk == -1) {
                    form.find('#id_question').attr('value', data);
                    if (display_alert) {
                        _alert('alert-success', 'Question saved successfully');
                    }
                } else {
                    if (display_alert) {
                        _alert('alert-success', 'Question updated successfully');
                    }
                }
                form.find('.alert').hide();
                save(question_id, data);
            } else {
                remove(question_id);
                var li = form.closest('li');
                var new_question = $(data).attr('id');
                li.html(data);
                var queued = undefined;
                if (!display_alert) {
                    queued = true;
                }
                question_change[question_id] = new_question;
                _alert('alert-warning', 'Error saving the question. For more details, click <a onclick="takemeto(\'' + new_question + '\');" href="#' + new_question + '">here</a>')
            }
        }
    });
}

function save_answer(element) {
    form = $(element).closest('form');
    no_pk = form.attr('id').charAt(form.attr('id').length - 1) == '_';
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        error: function (jqXHR, textStatus, errorThrown) {
            django_ajax_alert(jqXHR);
        },
        success: function (data) {
            if ($.isNumeric(data)) {
                if (no_pk) {
                    form.attr('action', form.attr('action') + data);
                    form.attr('id', form.attr('id') + data);
                }
            } else {
                var parent = form.parent();
                parent.html('');
                parent.before(data);
                parent.remove();
            }
        }
    });
}

function clean_table_modal() {
    table_modal = $('#id_table_body_modal');
    table_modal.find('input').removeAttr('value');
    table_modal.find('textarea').text('');
    table_modal.find('input').removeAttr('checked');
    table_modal.find('option').removeAttr('selected');
}

function save_table_answer(element) {
    form = $(element).closest('form');

    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        error: function (jqXHR, textStatus, errorThrown) {
            django_ajax_alert(jqXHR);
        },
        success: function (data) {
            $('#modal_add').modal('hide');
            $('body').removeClass('modal-open');
            $('.modal-backdrop').remove();
            var parent = form.parent();
            parent.replaceWith(data);
        }
    });
}

function edit_table(element, url) {
    form = $(element).closest('form');
    $.ajax({
        type: 'GET',
        url: url,
        error: function (jqXHR, textStatus, errorThrown) {
            django_ajax_alert(jqXHR);
        },
        success: function (data) {
            $('#modal_add').modal('hide');
            $('body').removeClass('modal-open')
            $('.modal-backdrop').remove();
            var parent = form.parent();
            parent.html(data);
        }
    });
}

function save_notes(element, url) {
    text = $(element).val();
    form = $(element).closest('form');
    no_pk = form.attr('id').charAt(form.attr('id').length - 1) == '_';

    $.ajax({
        type: 'POST',
        url: url,
        error: function (jqXHR, textStatus, errorThrown) {
            django_ajax_alert(jqXHR);
        },
        success: function (data) {
            if ($.isNumeric(data)) {
                if (no_pk) {
                    form.attr('action', form.attr('action') + data);
                    form.attr('id', form.attr('id') + data);
                }
            }
        }
    });
}