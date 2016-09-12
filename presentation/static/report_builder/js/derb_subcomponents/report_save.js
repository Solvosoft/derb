/**
 * Created by jaquer on 30/08/16.
 */

/*
 * Variables
 */
var categories = [];
var question_pool = [];
var categories_len = 0;
var saving = False;
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

function add_category(name, human_name) {
    categories[categories.length] = {
        'name': name,
        'order': categories_len,
        'human_name': human_name,
        'subcategories': [],
        'subcategories_len': 0
    };
    categories_len -= 1;
}

function add_subcategory(category, name, human_name) {
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
    delete category;

    category = [];
    var category_li = $('#categories_ul')[0].children;
    for (var x = 0; x < category_li.length; x++) {
        var category = $(li_category[x]).find('.category_admin')
        if (category.length != 0) {
            add_category($(category).attr('id').replace('categ_', ''), $(category).attr('title'));
        }
    }
}

function find_subcategories() {
    for (var x = 0; x < categories.length; x++) {
        var subcategory_div = $('#' + categories[x].name);
        var subcategory = subcategory_div.find('#ul_subcategories')[0].children;
        for (var y = 0; y < subcategory.length; y++) {
            var category = $(subcategory[y]).find('.subcategory_admin')
            if (category.length != 0) {
                add_subcategory(x, category.attr('id').replace('categ_', ''), category.attr('title'));
            }
        }
    }
}


function get_children(html_id) {
    find_html_children(html_id);
    return $($('#' + html_id + 'form')[0]).find('#id_children').val();
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
            for (var z = 0; z < categories[x].subcategories[y].question.length; z++) {
                process_question(categories[x].subcategories[y].question[z], counter);

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
        for (var z = 0; z < categories[y].subcategories.lenth; z++) {
            for (var w = 0; w < categories[y].subcategories[x].questions.length; w++) {
                categories[y].subcategories[z].question.push(
                    question_pool[get_question_from_id(categories[y].subcategories[z].questions[w])]
                );
            }
        }
    }
    put_question_number();
}

function save_questions() {
    find_categories();
    find_subcategories();
    for (var x = 0; x < categories.length; x++) {
        for (var y = 0; y < categories[x].subcategories.length; y++) {
            var name = categories[x].subcategories[x].name;
            var subcategory = $('#' + name);
            var question_li = subcategory[0].children[0].children;
            categories[x].subcategories[y].question = [];
            for (var z = 0; z < question_li.length; z++) {
                var question_div = $(question_li[z]).find('.question_panel')[0];
                if (question_div != undefined) {
                    
                }
            }
        }
    }
}