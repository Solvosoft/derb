/**
 * Created by jaquer on 30/08/16.
 */

/*
 * Variables
 */
var categories = [];
var question_pool = [];
var categories_len = 0;
var saving = false;
var last_element = 0;
var last_id = 0;
var question_change = {};

/*
 * Functions
 */
function submit_report_form() {
    var form = $('#report_form');
    form.find('#id_template').val(JSON.stringify(categories, null, 2));

    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            if (parseInt(data) == 1) {
                _alert('alert-succes', 'Report saved');
            } else {
                _alert('alert-danger', 'Report not saved');
            }
        },
        error: function (jqXHR, textStatus, errorThrown) {
            _alert('alert-warning', 'Code-related error: ' + jqXHR.status)
        }
    });
}

function save_ckeditor() {
    for (var key in CKEDITOR.instances) {
        var elem = $('#' + key);
        elem.html(CKEDITOR.instances[key].getData());
        elem.val(CKEDITOR.instances[key].getData());
    }
}

function add_question(pk, state, type, html_id) {
    question_pool.push({
        'pk': pk,
        'state': state,
        'type': type,
        'html_id': html_id,
        'saving': false
    });
    last_element = question_pool.length - 1;
    last_id = html_id;
}

function get_question_from_pool(id) {
    if (id != undefined) {
        var question = undefined;
        if (id == last_id) {
            return last_element;
        }

        for (var x = 0; x < question_pool.length && question == undefined; x++) {
            if (question_pool[x].html_id == id) {
                question = x;
                last_element = x;
                last_id = x;
            }
        }
    }
    return question;
}

function get_question_from_id(id) {
    var question = undefined;
    for (var x = 0; x < question_pool.length && question == undefined; x++) {
        if (question_pool[x].pk == id) {
            question = x;
        }
    }
    return question;
}

function add_category_to_categories(name, human_name) {
    categories[categories.length] = {
        'name': name,
        'order': categories_len,
        'human_name': human_name,
        'subcategories': [],
        'subcategories_len': 0
    };
    categories_len -= 1;
}

function add_subcategory_to_categories(category, name, human_name) {
    var subcategories_len = categories[category].subcategories_len;
    categories[category].subcategories[subcategories_len] = {
        'name': name,
        'human_name': human_name,
        'questions': [],
        'order': subcategories_len,
        'question': []
    };
    categories[category].subcategories_len = subcategories_len + 1;
}

function find_categories() {
    categories = [];

    var category_li = $('#ul_categories')[0].children;
    for (var x = 0; x < category_li.length; x++) {
        var category = $(category_li[x]).find('.admin_category');
        if (category.length != 0) {
            add_category_to_categories($(category).attr('id').replace('categ_', ''), $(category).attr('title'));
        }
    }
    find_subcategories();
}

function find_subcategories() {
    for (var x = 0; x < categories.length; x++) {
        var subcategory_div = $('#' + categories[x].name);
        var subcategory = subcategory_div.find('#ul_subcategories')[0].children;
        for (var y = 0; y < subcategory.length; y++) {
            var category = $(subcategory[y]).find('.admin_subcategory');
            if (category.length != 0) {
                add_subcategory_to_categories(x, category.attr('id').replace('categ_', ''), category.attr('title'));
            }
        }
    }
}

function get_children(html_id) {
    find_html_children(html_id);
    return $($('#' + html_id + ' form')[0]).find('#id_children').val();
}

function process_question(question, prefix) {
    if (question.type != 'simple_text' && question.type != 'model_info') {
        question.order = prefix;
        $($('#' + question.html_id + '#order')[0]).html(prefix);
        $($('#' + question.html_id + '#id_order')[0]).val(prefix);
        var counter = 1;
        var suffix = '';
        for (var child in question.children) {
            if (child != undefined) {
                for (var x = 0; x < question.children[child].length; x++) {
                    suffix = '';
                    if (question.children[child].length > 1) {
                        suffix = '.' + (x + 1);
                    }
                    process_question(question.children[child][x], prefix + '.' + counter + suffix)
                }
                counter += 1;
            }
        }
    } else {
        question.order = ' ';
    }
}

function put_question_number() {
    var counter = 1;
    for (var x = 0; x < categories.length; x++) {
        for (var y = 0; y < categories[x].subcategories.length; y++) {
            for (var z = 0; z < categories[x].subcategories[y].questions.length; z++) {

                process_question(categories[x].subcategories[y].questions[z], counter);

                if (categories[x].subcategories[y].questions[z].type != 'simple_text' &&
                    categories[x].subcategories[y].questions[z].type != 'model_info') {
                    counter += 1;
                }

            }
        }
    }
}

function build_tree() {
    var children = undefined;

    for (var x = 0; x < question_pool.length; x++) {
        children = get_children(question_pool[x].html_id);
    }

    for (var y = 0; y < categories.length; y++) {
        for (var z = 0; z < categories[y].subcategories.length; z++) {
            for (var w = 0; w < categories[y].subcategories[z].questions.length; w++) {
                var pool_id = get_question_from_id(categories[y].subcategories[z].questions[w]);
                categories[y].subcategories[z].question.push(question_pool[pool_id]);
            }
        }
    }
    put_question_number();
}

function save_questions() {
    find_categories();
    for (var x = 0; x < categories.length; x++) {
        for (var y = 0; y < categories[x].subcategories.length; y++) {
            var name = categories[x].subcategories[x].name;
            var subcategory = $('#' + name);
            var question_li = subcategory[0].children[0].children;
            categories[x].subcategories[y].question = [];
            for (var z = 0; z < question_li.length; z++) {
                var question_div = $(question_li[z]).find('.question_panel')[0];
                if (question_div != undefined) {
                    var key = $(question_div).attr('id');
                    var question_id = get_question_from_pool(key);

                    if (question_id != undefined) {
                        categories[x].subcategories[y].questions.push(
                            parseInt(question_pool[question_id].pk)
                        );
                    }
                }
            }
        }
    }
    build_tree();
    submit_report_form();
    saving = false;
}

function save_all_questions() {
    saving = true;
    categories = [];
    save_ckeditor();
    var json_data;

    var save_inmediatly = true;
    for (var qu = 0; qu < question_pool.length; qu++) {
        question_pool[qu].saving = true;
    }

    for (var q = 0; q < question_pool.length; q++) {
        if (question_pool[q].saving) {
            if ($('#' + question_pool[q].html_id).length != 0) {
                save_inmediatly = false;
                save_form(question_pool[q].html_id, true, false);
            } else {
                remove(question_pool[q].html_id);
            }
        }
    }

    if (save_inmediatly) {
        save_questions();
    }
}

function get_json_from_form(question_id) {
    var json_object = {};
    var question_div = $('#' + question_id);
    var question_form = question_div.find('form');
    var question_form_data = question_form.serializeArray();
    for (var i = 0; i < question_form_data.length; i++) {
        json_object[question_form_data[i].name] = question_form_data[i].value;
    }
    return json_object;
}

function set_modified_question(id) {
    var question_id = get_question_from_pool(id);
    if (question_id != undefined) {
        question_pool[question_id].state = 0;
    }
}

function save(id, pk) {
    var question_id = get_question_from_pool(id);
    if (question_id != undefined) {
        question_pool[question_id].state = 1;
        question_pool[question_id].pk = pk;
        var keep_going = true;
        if (saving) {
            for (var q = 0; q < question_pool.length && keep_going; q++) {
                if (question_pool[q].state == 0) {
                    keep_going = false;
                }
            }
            if (keep_going) {
                save_questions();
            }
        }
    }
}

function remove(id) {
    var question_id = get_question_from_pool(id);
    var parent = $('#' + id).closest('#questions').closest('.question_panel').attr('id');
    set_modified_question(parent);
    if (question_id != undefined) {
        question_pool.splice(question_id, 1);
        var children = $('#' + id).find('.question_panel');
        for (var c = 0; c < children.length; c++) {
            remove($(children[c].attr(id)));
        }
    }
}

function save_report() {
    save_all_questions();
}