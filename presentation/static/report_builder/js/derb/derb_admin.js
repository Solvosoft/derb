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
        var modal = $('#categories_delete_modal').clone();
        var html = modal.html().replace(/text/gi, text).replace(/id_name/gi, category_id);

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
    var dialog = $('#question_delete_modal').clone();
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

function load_category(select, change) {
    see_hide_combo(select);
    if (change == 1) {
        questions = $($(select).closest('.question_panel').find('#questions')[0]);
        catalog = $(select).find(':selected').val();

        $.getJSON('/derb/catalog/' + catalog, function (data) {
            text = '<ul>';
            $.each(data, function (key, val) {
                text += "<li id='" + key + "'><h4>" + val + "</h4>";
                text += "<ul class=\"sortable\"><li>Drag and drop here aquí</li></ul>";
                text += '</li>';
            });
            text += '</ul>';
            questions.html(text);
            do_sortable();
        });
    }
}

function add_update_category() {
    var category_func = 'onDblClick="edit_category_text(this);"';
    var subcategory_func = 'onDblClick="edit_subcategory_text(this);"';
    var category_id = 'end_categories';
    var subcategory_id = 'end_subcategories';

    var new_nav = '<li [func]> <button type="button" onclick="delete_category(this);" class="close_category btn" aria-hidden="true">&times;</button>\
	               <a [class] title="[help]" data-toggle="tab" href="#[name]" id="categ_[name]">[text]</a></li>';

    var new_subcategory_content = '<div class="tab-pane [sub_active] class_subcategoria" id="[category_name]">\
                                    <ul class="sortable list-group">\
                                        <li class="list-group-item">Drag and drop your questions here</li></ul>\
                                    </div>';
    var new_category_content = ' <div  class="tab-pane class_categoria" id="[name]">\
                            <ul id="ul_subcategories" class="subcategory nav nav-tabs">\
                            <li ' + subcategory_func + ' class="active">\
                            <button type="button" onclick="delete_category(this);" class="close_category btn" aria-hidden="true">&times;</button>\
                            <a id="categ_[category_name]" class="admin_subcategory" href="#[category_name]" data-toggle="tab" title="[help]">[text]</a></li>\
                            <li id="end_subcategories" class="btn btn-success" onclick="add_subcategory(this);" title="Add subcategory"> <span class="glyphicon glyphicon-plus-sign"></span></li></ul>\
                            <div class="tab-content">' + new_subcategory_content + '</div></div>';

    var modal = $('#categories_modal');
    var input = $(modal).find('#category_modal_update');
    var text = input.val();
    var name = input.attr('name');
    var type = $(modal.find('#modal_category_type')[0]);
    var type_name = type.attr('name');
    var type_value = type.val();
    var help = text;

    if (text.length > 20) {
        text = text.substr(0, 20);
    }

    if (name != '') {
        if (type_name == 'category') {
            cat = $($('#ul_categories').find('.active').find('a')[0]);
            cat.html(text);
            cat.attr('title', help);
        } else {
            var div = $('#' + type_value);
            cat = $($(div.find('.active')[0]).find('a')[0]);
            cat.html(text);
            cat.attr('title', help);
        }
    } else {
        var end = category_id;
        var pre = '';
        var type_id = category_id;
        var content = $.find('#category_content')[0];
        var begin = $;
        var func = category_func;
        var klass = 'class="admin_category"';

        if (type_name == 'subcategory') {
            end = subcategory_id;
            pre = type_value + '_';
            new_category_content = new_subcategory_content;
            type_id = subcategory_id;
            func = subcategory_func;
            begin = $('#' + type_value);
            klass = 'class="admin_subcategory"';
            var selector = '#' + type_value + ' .tab-content';
            content = $($('#' + type_value + ' .tab-content')[0]);
        }

        var end_nav = $(begin.find('#' + end)[0]);

        var ul = end_nav.closest('ul');
        name = pre + 'categ' + ul.children().length;
        var category_name = name;
        var sub_active = '';
        if (type_name == 'category') {
            category_name = name + '_start';
            sub_active = 'active';
        }

        var final_nav = new_nav.replace(/\[text\]/gi, text).replace(/\[name\]/gi, name).replace(/\[help\]/gi, help).replace(/\[func\]/gi, func).replace(/\[class\]/gi, klass);

        var final_content = new_category_content.replace(/\[text\]/gi, text).replace(/\[name\]/gi,
            name).replace(/\[type_id\]/gi, type_id).replace(/\[category_name\]/gi,
            category_name).replace(/\[sub_active\]/gi, sub_active).replace(/\[help\]/gi, help);

        end_nav.before(final_nav);
        $(content).append(final_content);
    }

    sort_categories();
    sort_subcategories();
    modal.modal('hide');
    do_sortable();
}

function hide_if_enter(mi, event) {
    var keycode = event.which;
    if (keycode == 13) {
        $(mi).closest('#modal_categorias').find('#bgm').click();
    }
}