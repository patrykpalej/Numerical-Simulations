import streamlit.components.v1 as components


def change_widget_font_size(widget, wch_font_size='12px'):
    htmlstr = """<script>var elements = window.parent.document.querySelectorAll('*'), i;
                    for (i = 0; i < elements.length; ++i) { if (elements[i].innerText == |wgt_txt|) 
                        { elements[i].style.fontSize='""" + wch_font_size + """';} } </script>  """

    htmlstr = htmlstr.replace('|wgt_txt|', "'" + widget + "'")
    components.html(f"{htmlstr}", height=0, width=0)
