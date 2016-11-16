/**
 * Created by jaquer on 05/09/16.
 */

function save_question_sinchronously(question_id) {
    json_data = get_json_from_form(question_id);
    save_form(question_id, json_data, false, false);
    var pool_id = get_question_from_pool(question_id);

    if (pool_id == undefined) {
        pool_id = get_question_from_pool(question_change[question_id]);
    }

    var result = parseInt(question_pool[pool_id].pk);

    if (result == -1) {
        throw new Error('Unanswered question');
    }

    return result;
}

function load_questions_id(list) {
    var txt = [];
    var question_id = '';
    var question_list = [];
    var qid = -1;
    var qnumber = -1;

    for (var x = 0; x < list.length; x++) {
        question_id = $($(list[x]).find('.question_panel')[0]);
        if (question_id.length > 0) {
            question_id = $($(question_id[0]).find('#question_id')[0]);

            if (question_id.val() != "") {
                txt.push(parseInt(question_id.val()));
                find_children_id(question_id.val());
                qid = get_question_from_id(question_id.val());
            } else {
                var question = question_id.closest('.question_panel').attr('id');
                qnumber = save_question_sinchronously(question);
                qid = get_question_from_id(qnumber);
                txt.push(qnumber);
            }
            question_list.push(question_pool[qid]);
        }
    }
    return {
        'txt': txt,
        'question_list': question_list
    };
}

function load_simple_text_question(content, html_id) {
    /* TODO */
}

function load_boolean_question(content, html_id) {
    var target_question = get_question_from_pool(html_id);
    question_pool[target_question].children = {};

    var question_id = content.closest('.question_panel').attr('id');
    var yes_list = load_questions_id($(content.find('#' + question_id + '_yes ul')[0]).children());
    var no_list = load_questions_id($(content.find('#' + question_id + '_no ul')[0]).children());
    var nr_list = load_questions_id($(content.find('#' + question_id + '_nr ul')[0]).children());

    question_pool[target_question].children['yes'] = yes_list.question_list;
    question_pool[target_question].children['no'] = no_list.question_list;
    question_pool[target_question].children['nr'] = nr_list.question_list;

    var result = {
        'yes': yes_list.txt,
        'no': no_list.txt,
        'nr': nr_list.txt
    };

    return JSON.stringify(result, null, 2);
}

function load_model_selection_question(content, html_id) {
    /* TODO */
}

function load_numeric_question(content, html_id) {
    /* TODO */
}

function load_question_info(content, html_id) {
    /* TODO */
}

function get_question_children_id(content, type, html_id) {
    var answer = "";

    if (type == 'conditional_model') {
        answer = load_model_selection_question(content, html_id);
    } else if (type == 'boolean_question') {
        answer = load_boolean_question(content, html_id);
    } else if (type == 'float_question' || type == 'decimal_question') {
        answer = load_numeric_question(content, html_id);
    } else if (type == 'simple_text_question') {
        answer = load_simple_text_question(content, html_id);
    } else if (type == 'question_info') {
        answer = load_question_info(content, html_id);
    }

    return answer;
}

function load_subquestions(form, html_id) {
    var type = form.find('#name').val();
    var content = form.closest('.question_panel').find('#questions');
    var children = get_question_children_id(content, type, html_id);
    form.find('#id_children').val(children);
}

function find_html_children(question_id) {
    var form = $($('#' + question_id + ' form')[0]);
    load_subquestions(form, question_id);
}

function find_children_id(id) {
    find_html_children(get_question_from_id(id).html_id);
}