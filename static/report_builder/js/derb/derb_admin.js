/**
 * Created by jaquer on 05/09/16.
 */

active_category = active_subcategory = 'default';

function rename_subcategories(current_category, new_category) {
    var ul_subcategory = $('#' + current_category + '#subcategories_ul li a');

    for (var x = 0; x < ul_subcategory.length; x++) {
        $(ul_subcategory[x]).attr('id', 'categ_' + new_category + '_categ' + x);
        var ref = $(ul_subcategory[x]).attr('href');
        $(ul_subcategory[x]).attr('href', 'categ_' + new_category + '_categ' + x);
        $(ref).attr('id', new_category + '_categ' + x);
    }
}

function delete_category_by_name(name) {
    var li = $(name).closest('li');
    var category_list = li.closest('ul');
    var type = category_list.attr('id');
    var the_victim = li.find('a').attr('id').replace('categ_', '#');
    li.remove();
    var questions = $(the_victim).find('.question_panel');
    for (var q = 0; q < questions.length; q++) {
        remove($(questions[q]).attr('id'));
    }

    if (type == 'categories_ul') {
        $(the_victim).remove();
        var categories = $('#categories_ul li a');
        for (var c = 0; c < categories.length; c++) {
            var href = $(categories[c]).attr('href');
            var current_category = href.replace('#', '');
            rename_subcategories(current_category, 'categ' + c);
            $(categories[x]).attr('id', 'categ_categ' + c);
            $(categories[x]).attr('href', '#categ' + c);
            $(href).attr('id', 'categ' + c);
        }
    } else if (type == 'subcategories_ul') {
        var category = category_list.closest('.tab-pane').attr('id');
        $(the_victim).remove();
        rename_subcategories(category, category);
    }
}

function delete_category(button) {
    var ul = $(button).closest('ul');
    if (ul.children().length < 3) {
        _alert('alert-warning', 'There must be at least one category or subcategory');
    } else {
        var category = $($(button).closest('li').find('a')[0]);
        var text = category.attr('title');
        var category_id = category.attr('id');
        var modal = $('#rm_categories_modal').clone();
        var html = modal.html().replace(/text/gi, texto).replace(/id_name/gi, category_id);

        modal.html(html);
        modal.modal('show').bind('closed.bs.alert', function () {
            this.remove();
        });
    }
}

function take_me_to(id) {
    var question = $('#' + id);
    var subcategory_div = $(question.closest('.subcategory_class')[0]).attr('id');
    var subcategory = $('#categ_' + subcategory_div);
    var category_div = $(subcategory.closest('.category_class')[0]).attr('id');
    var categor = $('#categ_' + category_div);
    category.click()
    subcategory.click();
}

function table_changes(input) {
    set_modified_question($(input).closest('.question_panel').attr('id'));
}

function add_column(button, model) {
    set_modified_question($(button).closest('.question_panel').attr('id'));

    container = $(button).closest('.container');
    hidden = container.find('#field_select').html();
    table = container.find('#values');
    row = table.find('#add');
    title = table.find('#add_title');
    quantity = $($(table.children()[0]).children()[0]).children().length;
    select_id = model + '_select_' + quantity;
    hidden = hidden.replace(model + '_select_', select_id);

    row.before('<td>' + hidden + '</td>');
    title.before($('<th class="info"><span class="glyphicon glyphicon-remove pull-right" onclick="delete_column(this);"></span> \
	 <input type="text" onchange="table_changes(this);" class="form-control" value="" name="' + model + '_enc_' + quantity + '" placeholder="Header here"></th>'));

    return false;
}

function delete_column(selected) {
    set_modified_question($(selected).closest('.question_panel').attr('id'));

    var parent = $(selected).parent();
    var parent_tr = parent.parent();
    var selected_tr = $(tr_parent.next());
    var children_tr = parent_tr.children();
    var children_selected_tr = selected_tr.children();
    var index = children_tr.index(parent);

    var count = 0;
    if (index > 0) {
        children_tr[index].remove();
        children_selected_tr.remove();
        for (var x = 0; x < children_tr.length - 1; x++) {
            if (x != index) {
                var splitted_name = $(children_tr[x]).find('input').attr('name').split('_');
                var name = splitted_name.slice(0, splitted_name.length - 1).join('_') + '_' + (count + 1);
                $(children_tr[x]).find('input').attr('name', name);

                var splitted_name = $(children_selected_tr[x]).find('select').attr('name').split('_');
                var name = splitted_name.slice(0, splitted_name.length - 1).join('_') + '_' + (count + 1);
                $(children_selected_tr[x]).find('select').attr('name', name);
                count++;
            }
        }
    }
}

function modify_parent(list) {
    var parent = list.closest('#questions');
    if (parent.length > 0) {
        var question = parent.closest('.question_panel').attr('id');
        set_modified_question(question);
        modify_parent($('#' + question));
    }
}

function cke_onchange(e) {
    set_modified_question($('#' + e.editor.name).closest('.question_panel').attr('id'));
}

function set_cke_onchange(editor_id) {
    CKEDITOR.instances[editor_id].on('change', cke_onchange);
}

function do_sortable() {
    $('.sortable').sortable({
        connectWith: '.sortable',
        receive: function (event, ui) {
            if (ui.item.hasClass('palette_item')) {
                new_item = ui.item.clone();
                ui.item.removeClass('palette_item');
                ui.item.load(ui.item.attr('url'));
                ui.item.attr('id', '');
                ui.item.attr('style', '');
                var order = parseInt(new_item.attr('order'));
                var before = ui.sender.find('[order=' + (order - 1) + ']');
                var after = ui.sender.find('[order=' + (order + 1) + ']');

                if (before.length == 0) {
                    after.before(new_item);
                } else {
                    before.after(new_item);
                }
            }
            modify_parent(ui.item.parent());
        },
        start: function (event, ui) {
            set_modified_question(ui.item.closest('#questions').closest('.question_panel').attr('id'));

            rebuild = [];
            var cke_editors = $(ui.item).find('.question_panel .cke');
            for (var i = 0; i < cke_editors.length; i++) {
                var editor = $(cke_editors[i]);
                var editor_id = editor.attr('id').replace('cke_', '');
                rebuild.push(editor_id);
                $('#' + editor_id).html(CKEDITOR.instances[editor_id].getData());
                CKEDITOR.instances[editor_id].destroy();
            }
        },
        stop: function (event, ui) {
            for (var x = 0; x < rebuild.length; x++) {
                var question_id = $('#' + rebuild[x]).closest('.question_panel').attr('id');
                var cke_params = ckeditor_conf.empty;
                var question = get_question_from_pool(question_id);
                var qtype = question_pool[question].type;
                if (qtype == 'model_info' || qtype == 'simple_text' || qtype == 'question_info') {
                    cke_params = ckeditor_conf.basic;
                }
                CKEDITOR.replace(rebuild[x], cke_params);
                CKEDITOR.instances[rebuild[x]].on('change', cke_onchange);
            }
            rebuild = [];
        }
    });
}

function delete_question_admin(question_ids) {
    var ids = question_ids.split(',');
    var id = '#' + ids[0];
    var li = $(id).closest('li');
    var ul = li.closest('ul');

    for (var x = ids.length - 1; x >= 0; x--) {
        remove(ids[x]);
        $('#' + ids[x]).remove();
    }

    li.remove();
    if (ul.children().length == 0) {
        ul.append('<li class="list-group-item">Drag and drop your questions here</li>')
    }
}

function delete_question(button) {
    var question = $(button).closest('.question_panel');
    var dialog = $('#delete_question_modal').clone();
    var forms = question.find('form');
    var text = '<ul>';
    var question_id = '$';

    for (var x = 0; x < forms.length; x++) {
        var value = $($(forms[x]).find('#id_text')[0]).val();
        if (value == undefined || value == '') {
            value = 'Unnamed question';
        }
        text += '<li>' + value + '</li>';
        question_id += ',' + $(forms[x]).closest('.question_panel').attr('id');
    }
    question_id = question_id.replace('$,', '');
    text += '</ul>';

    var html = dialog.html().replace(/text/gi, text).replace(/id_name/gi, question_id);
    dialog.html(html);
    dialog.modal('show').bind('closed.bs.alert', function () {
        this.remove();
    });
}

function sort_categories() {
    $('#ul_categories').sortable({
        connectWith: '#ul_categories',
        cancel: '#end_categories'
    });
}

function sort_subcategories() {
    $('.subcategory').sortable({
        connectWith: '.subcategory'
    });
}