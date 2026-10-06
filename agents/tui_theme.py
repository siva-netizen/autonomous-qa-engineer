"""Green terminal theme for the QA engineer TUI."""

GREEN_THEME_CSS = """
Screen {
    background: #061206;
}

Header {
    background: #0f3d0f;
    color: #b8ffb8;
    text-style: bold;
}

Footer {
    background: #0a2a0a;
    color: #6fdc6f;
}

Footer > FooterKey {
    background: #0f3d0f;
    color: #9dff9d;
}

Footer > FooterKey:hover {
    background: #1a5c1a;
}

#chat {
    height: 1fr;
    border: tall #1faa59;
    background: #081808;
    padding: 1 2;
    scrollbar-color: #1faa59;
    scrollbar-background: #0a200a;
}

#prompt {
    dock: bottom;
    margin: 0 0 1 0;
    border: tall #2ecc71;
    background: #0a220a;
    color: #d6ffd6;
}

#prompt:focus {
    border: tall #58ff58;
}

StreamPreview {
    dock: bottom;
    margin: 0 1;
}

ActivityRail {
    dock: bottom;
    height: auto;
    min-height: 3;
    background: #0c320c;
    border-top: solid #2ecc71;
    padding: 0 1 1 1;
    margin: 0 1;
}

ActivityRail.-pulse #activity-text {
    text-style: bold;
    color: #58ff58;
}

ActivityRail #activity-head {
    height: 1;
}

ActivityRail LoadingIndicator {
    width: 3;
    height: 1;
    color: #43ff43;
}

ActivityRail #activity-text {
    width: 1fr;
    color: #8dff8d;
}

ActivityRail #tool-trail {
    color: #6fdc6f;
    padding-left: 4;
}

IdleStatusRail {
    dock: bottom;
    height: 1;
    margin: 0 1;
}

.user-line {
    color: #7dffb8;
}

.assistant-line {
    color: #c8ffc8;
}
"""
