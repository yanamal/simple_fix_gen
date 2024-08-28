function wrap_text_in_spans(selection, span_class) {
    $('.ast-node', selection).contents().filter(function() {
        return this.nodeType == Node.TEXT_NODE
    }).each(function(){
        let text_span = document.createElement('span')
        text_span.innerHTML=this.textContent
        text_span.className = span_class
        this.parentNode.insertBefore(text_span, this)
        this.parentNode.removeChild(this);
    })
}

function highlight_nodes() {
    $('.ast-node').mouseover(function(e)
        {
            e.stopPropagation();
            const node_id = $(this).attr('data-node-id')

            $('.ast-node').removeClass('highlight'); // stop highlighting everything else

            $(`[data-node-id="${node_id}"]`).addClass('highlight');
        });

    $('.ast-node').mouseout(function(e)
        {
            const node_id = $(this).attr('data-node-id')
            $(`[data-node-id="${node_id}"]`).removeClass('highlight');
        });
}


function update_values_shown(before_pre, after_pre, trace, new_i) {
    $('.code-block .ast-node').removeClass('evaluated-node')
    $('.code-block .ast-node>.value').remove()


    if(trace[new_i]['before']) {
        let before_node = $(`[data-node-id="${trace[new_i]['before']['node']}"]`, before_pre)
        before_node.addClass('evaluated-node')
        let value_span = $('<span>', {class: "value"}).text(trace[new_i]['before']['values'])
        before_node.prepend(value_span)
    }

    if(trace[new_i]['after']) {
        let after_node = $(`[data-node-id="${trace[new_i]['after']['node']}"]`, after_pre)
        after_node.addClass('evaluated-node')
        let value_span = $('<span>', {class: "value"}).text(trace[new_i]['after']['values'])
        after_node.prepend(value_span)
    }
}

function generate_trace(step_data) {
    // let before_pre =  $('<pre/>', {class: 'trace-block before-fix-trace'}).html(step_data['source'])
    let before_pre = $('#before_block')
    // let after_pre =  $('<pre/>', {class: 'trace-block after-fix-trace'}).html(step_data['dest'])
    let after_pre = $('#after_block')

    let explanation = $(
        `<div class="explanation"> Comparing the effect of executing <pre>${step_data['unit_test_string']}</pre> with and without this fix</div><br/>
        <div class="explanation">${correction_data['effect_summary']}</div>
        <hr/>`)

    let slider_id = `trace-slider-correction`
    let slider = $('<div/>', {class: 'trace-slider', id: slider_id})

    let trace_contents = $('<div/>', {class: 'trace-div'})

    trace_contents.append(explanation)

    let comparison_div = $('<div/>', {class: 'comparison-div'})
    trace_contents.append(comparison_div)

    comparison_div.append(before_pre)
    comparison_div.append(slider)
    comparison_div.append(after_pre)

    let update_listener = function( event, ui ) {
            let op_index = -ui.value
            update_values_shown(before_pre, after_pre, step_data['synced_trace'], op_index)
            console.log( step_data['synced_trace'][op_index])
        }

    // decide which point of interest to jump to on the slider:
    let slider_initial = step_data['points_of_interest']['last_matching_before_fix']  // default to the last correct thing evaluated (should always be there?)
    if(step_data['points_of_interest']['first_wrong_before_fix']){
        // prefer the first point where an explicitly wrong value is produced (if one exists)
        slider_initial = step_data['points_of_interest']['first_wrong_before_fix']
        console.log(`correction trace: using first_wrong_before_fix`)
    }
    else if(step_data['points_of_interest']['exception_before_fix']) {
        // next, prefer highlighting the fact that an exception was thrown before the fix
        slider_initial = step_data['points_of_interest']['exception_before_fix']
        console.log(`correction trace: using exception_before_fix`)
    }
    else if(step_data['points_of_interest']['last_matching_after_fix'] > step_data['points_of_interest']['last_matching_before_fix']) {
        // next preference is for showing a time the after-fix version did something right,
        // if it was strictly later than the last time that the before-fix version did something right
        slider_initial = step_data['points_of_interest']['last_matching_after_fix']
        console.log(`correction trace: using last_matching_after_fix`)
    }
    else if(step_data['points_of_interest']['last_matching_before_fix']+1 < step_data['synced_trace'].length) {
        // final not-quite-default heuristic:
        // if there's *anything* after the last time that the before-fix code was correct, show that
        slider_initial = step_data['points_of_interest']['last_matching_before_fix']+1
        console.log(`correction trace: using step after last_matching_before_fix`)
    }

    // use negative step values for the slider to make it go from top to bottom
    slider.slider({
        orientation: "vertical",
        range: "max",
        min: -step_data['synced_trace'].length+1,
        max: 0,
        value: -slider_initial,
        change: update_listener,
        slide: update_listener
    });

    let ticks = $('<div/>', {class:'ticks'})
    for(let op of step_data['synced_trace']) {
        let before_line_class = "no-op-line"
        if(op['before']) {
            if(op['before']['values'].length <= 0 || op['value_matches']) {
                before_line_class = "op-line"
            }
            else {
                before_line_class = "bad-value-op-line"
            }
        }

        let after_line_class = "no-op-line"
        if(op['after']) {
            if(op['after']['values'].length <= 0 || op['value_matches']) {
                after_line_class = "op-line"
            }
            else {
                after_line_class = "bad-value-op-line"
            }
        }

        ticks.append($(`
<span class="tick">
    <svg height="1" width="100%">
        <line x1="0" y1="0" x2="10" y2="0" class="${before_line_class}"></line>
        <line x1="30" y1="0" x2="40" y2="0" class="${after_line_class}"></line>
    </svg>
</span>`))

    }
    slider.append(ticks)

    return trace_contents
}



$(document).ready(function() {
    wrap_text_in_spans($('pre'), 'text-span')
    let trace_div = generate_trace(correction_data)
    $('body').append(trace_div)
    $('.trace-slider').each(function(){
        $(this).slider("value", $(this).slider("value"));
        $(this).height($(this).parent().height()-10)
    })
    highlight_nodes()
})