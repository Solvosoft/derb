/**
 * Created by jaquer on 09/08/16.
 */

/**
 * Variables
 */
var max_message_queue = 3;
var last_type = '';
var otables = {};

$(document).ready(function () {
    $('.sortable-palette').sortable({
        connectWith: '.sortable'
    });

    $('#categories_modal').modal('hide');

    $('#id_opening_date').datepicker({
        'dateFormat': 'dd/mm/yy'
    });
});

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

function rearrange_options(html_id) {
    var element = $('#' + html_id);
    var option = element.find('.contain_schema')[0];
    $(element.find('#no_schema')[0]).append(option);
}

function get_cookie(name) {
    var cookie_value = null;

    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);

            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookie_value = decodeURIComponent(cookie.substring(name.length + 1));
            }
        }
    }
    return cookie_value;
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

function delete_question_table_row(element, url, form_number) {
    dialog = $('<div id="dialog-confirm" title="Delete">\
		<p><span class="ui-icon ui-icon-alert" style="float:left; margin:20px 10px 20px 0;"></span>\
		This operation is irreversible: are you sure you want to delete this element?</p></div>');

    dialog.dialog({
        resizable: false,
        height: 200,
        open: function () {
            var close_button = $('.ui-dialog-titlebar-close');
            close_button.append('<span class="ui-button-icon-primary ui-icon ui-icon-closethick"></span>');
        },
        close: function () {
            $(this).remove();
        },
        buttons: {
            'No': function () {
                $(this).dialog('close');
            },
            'Yes': function () {
                $(this).dialog('close');
                var current_table = $(element).closest('tbody');
                var to_delete = $($('table tbody')[0]).find('.eliminator');
                for (var x = 0; x < to_delete.length; x++) {
                    if (element == to_delete[x]) {
                        url += x;
                        x = to_delete.length;
                    }
                }

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: {
                        'csrfmiddlewaretoken': get_cookie('csrftoken')
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        django_ajax_alert(jqXHR);
                    },
                    success: function (data) {
                        if (data == 'True') {
                            otable = otables['dataTb_' + form_number];
                            var position = otable.fnGetPosition($(element).closest('tr').get(0));
                            otable.fnDeleteRow(parseInt(position));
                        } else {
                            _alert('alert-warning', 'The element could not be deleted, please try again.');
                        }
                    }
                })
            }

        }
    });
}

function see_hide(button) {
    panel = $(button).closest('.question_panel');
    body = panel.find('.panel-body');
    content = panel.find('#content');

    body.toggle();
    content.toggle();
}

function see_hide_combo(combo) {
    option = $(combo);
    content = option.closest('.question_panel');
    options = content.find('#properties');
    selected_option = option.find(':selected').val();
    for (var i = 0; i < options.children().length; i++) {
        $(options.children()[i]).attr('class', 'hidden');
    }
    options.find('#' + selected_option).attr('class', 'container');
}

function fill_names(value, name, name_type, value_type) {
    modal = $('#categories_modal');
    var input = $(modal.find('#category_modal_update')[0]);
    var type = $(modal.find('#modal_category_type')[0]);

    input.val(value);
    input.attr('name', name);
    type.attr('name', name_type);
    type.val(value_type);
}

function edit_category_text(li) {
    var nav = $($($(li)[0]).find('a'));
    var text = nav.attr('title');
    var name = nav.attr('href');

    fill_names(text, name, 'category', '');
    $('#categories_modal').find('#categories_modal').text('Edit category');
    modal.modal();
}

function edit_subcategory_text(li) {
    var div = $(li).closest('div');
    var category = div.attr('id');
    nav = $($($($(li)[0]).find('a'))[0]);
    var text = nav.attr('title');
    var name = nav.attr('href');
    fill_names(text, 'aa', 'subcategory', category);
    $('#categories_modal').find('#categories_modal').text('Edit subcategory');
    modal.modal();
}

function add_category() {
    fill_names('', '', 'category', '');
    $('#categories_modal').find('#categories_modal').text('Add category');
    modal.modal();
}

function add_subcategory(li) {
    var div = $(li).closest('div');
    var category = div.attr('id');
    fill_names('', '', 'subcategory', category);
    $('#categories_modal').find('#categories_modal').text('Add subcategory');
    modal.modal();
}

function clean_modal() {
    fill_names('', '', 'category', '');
    modal.modal('hide');
}

function show_related_question(element) {
    var parent_form = $(element).closest('form');
    var question_id = parent_form.find('#id_question').val();
    var objects = parent_form.find(':checkbox');
    var selected_options;

    if (objects.length > 0) {
        selected_options = parent_form.find('input:checked');
    } else {
        objects = parent_form.find('select option');
        selected_options = parent_form.find('select option:select')
    }

    objects.each(function (index, value) {
        $('#' + question_id + '_' + $(value).val()).hide();
    });

    selected_options.each(function (index, value) {
        $('#' + question_id + '_' + $(value).val()).show();
    });
}

function set_related_question(form) {
    var objects = $(form).find(':checkbox');
    var selected_options = undefined;
    var option = false;
    if (objects.length == 0) {
        objects = $(form).find('select');
        selected_options = $(form).find('select option:selected');
        option = true;
    } else {
        selected_options = $(form).find('input:checked');
    }

    objects.each(function (index, value) {
        $(value).attr('onchange', 'show_related_question(this)');
    });

    if (selected_options.length > 0) {
        show_related_question(selected_options[0]);
    }
}

function show_related_boolean_question(id) {
    var list = $(id).closest('ul');
    var type = list.find('input:checked').val();
    var qid = list.closest('form').find('#id_question').val();

    $($('#' + qid + '_nr')[0]).hide();
    $($('#' + qid + '_yes')[0]).hide();
    $($('#' + qid + '_no')[0]).hide();
    $($('#' + qid + '_' + type)[0]).show();
}

function show_related_numeric_question(element, id) {
    $($(id + '_question_max')[0]).hide();
    $($(id + '_question_no_max')[0]).hide();

    if ($(element).attr('aria-valuenow') != undefined) {
        if (parseFloat($(element).attr('aria-valuenow')) >= parseFloat($(element).attr('aria-valuemax'))) {
            $($(id + '_question_max')[0]).show();
        } else {
            $($(id + '_question_no_max')[0]).show();
        }
    }
}