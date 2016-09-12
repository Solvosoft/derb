/**
 * Created by jaquer on 05/09/16.
 */

function save_question_sinchronously(question_id) {
    
}

function get_question_children_id(content, type, html_id) {
    var answer = "";
    /**
     * TODO: Questions processing according to type
     */
    return answer;
}

function load_subquestions(form, html_id) {
    var type = form.find('#name').val();
    var content = form.closest('.question_panel').find('#questions');
    var children = get_question_children_id(content, type, html_id);
    form.find('#id_children').val(children);
}

function find_html_children(question_id) {
    var form = $($('#' + question_id + '_form')[0]);
    load_subquestions(form, question_id);
}

function find_children_id(id) {
    //find_html_children()
}