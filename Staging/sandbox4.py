# import time
# import threading
#
# from gi.repository import Gtk, Gdk, GObject
#
# window = None
#
# def main():
#     GObject.threads_init()
#     Gdk.threads_init()
#
#     # Build GUI:
#     global window
#     window = Gtk.Window()
#     button = Gtk.Button(label="Click me")
#     window.add(button)
#     window.set_default_size(200, 200)
#     window.show_all()
#
#     # Connect signals:
#     window.connect("delete-event", Gtk.main_quit)
#     button.connect("clicked", on_button_click)
#
#     Gtk.main()
#
# def on_button_click(button):
#     print "Debug on_button_click: current_thread name:", threading.current_thread().name
#
#     # This is a callback called by the main loop, so it's safe to
#     # manipulate GTK objects:
#     watch_cursor = Gdk.Cursor(Gdk.CursorType.WATCH)
#     window.get_window().set_cursor(watch_cursor)
#     button.set_label("Working...")
#     button.set_sensitive(False)
#
#     def lengthy_process():
#         print "Debug lengthy_process: current_thread name:", threading.current_thread().name
#         # We're in a new thread, so we can run lengthy processes without
#         # freezing the GUI, but we can't manipulate GTK objects except
#         # through GObject.idle_add
#         time.sleep(10)
#         def done():
#             print "Debug done: current_thread name:", threading.current_thread().name
#             window.get_window().set_cursor(None)
#             button.set_label("Done!")
#             return False
#         GObject.idle_add(done)
#
#     thread = threading.Thread(target=lengthy_process)
#     thread.start()
#
# if __name__ == "__main__":
#     main()

thisset = set()
thisset.add("turd")
print(thisset)



#############################################
https://stackoverflow.com/questions/52436541/how-to-retrieve-data-from-blocking-read-in-another-thread-in-gtk3/52480019#52480019

 finally solved my problem by following pan-mroku's suggestion, i.e. by using IO Channels on a pipe opened with popen.

This is the relevant code which is, in the end, able to read information from the server as new lines, with new data, are printed to stdout by the server itself, and update the GTK+ GUI accordingly.

# include <gtk/gtk.h>
# include <errno.h>
// ...

static
gboolean
serverParser(GIOChannel * source, GIOCondition
condition, gpointer
data) {
    gchar * linebuf;
gsize
strsize_linebuf;
GIOStatus
opstatus;
int
scan_retval = 0;
// ...

opstatus = g_io_channel_read_line(source, & linebuf, & strsize_linebuf, NULL, NULL);
if (opstatus == G_IO_STATUS_NORMAL & & strsize_linebuf != 0) {
scan_retval=sscanf(linebuf, "%c %*s %f%*[- *]%f %*s %*f %*s %lf %c%*s %*f %*s %*f%*[/ *]%d %*s", & field_1, & field_2, & field_3, & field_4, & field_5, & field_6);

if (scan_retval == 6) {
// Work with the parsed server data, line by line
}
}

//...

g_free(linebuf);
return TRUE;
}



static
void
start_server(GtkWidget * widget, gpointer
data) {
// ...
FILE * iperfFp;
int
iperfFd;
GIOChannel * iperfIOchannel;

// ...
// Start
server
using
stdbuf
to
get
a
line
buffered
output
iperfFp = popen("stdbuf -o L iperf -s -u", "r");

if (!iperfFp) {
g_print("Error in launching the server. errno = %d\n", errno);
return;
}

iperfFd = fileno(iperfFp);

iperfIOchannel = g_io_channel_unix_new(iperfFd);
g_io_channel_set_flags(iperfIOchannel, G_IO_FLAG_NONBLOCK, NULL);
g_io_channel_set_line_term(iperfIOchannel, NULL, -1);
g_io_add_watch(iperfIOchannel, G_IO_IN, serverParser, & (data_struct->parser_pointers));

// ...
}

// ...

When the start button is clicked, the start_server callback is invoked, which starts the iPerf server (but the same could be done for any other external process) with popen and configures a new IO Channel. Then, every time a new line is generated by the server itself, serverParser is called to parse all the relevant data.

I had to start the external iPerf process by invoking stdbuf first (with the argument -o L), in order to get a line buffered output and have serverParser called for each line generated by that process.




Here is an example in Perl in case someone should be interested. This just shows the basic principle of how to do asynchronous things within the GTK event loop:

#! /usr/bin/env perl
use feature qw(say);
use strict;
use warnings;

use Glib 'TRUE', 'FALSE';
use Gtk3 -init;
use AnyEvent;  # Important: load AnyEvent after Glib!
use AnyEvent::Subprocess;

use constant {
    GTK_STYLE_PROVIDER_PRIORITY_USER => 800,
};

my $window = Gtk3::Window->new( 'toplevel' );
my $grid1 = Gtk3::Grid->new();
$window->add( $grid1 );
my $frame1 = Gtk3::Frame->new('Output');
$frame1->set_size_request(800,600);
$grid1->attach($frame1, 0,0,1,1);
my $scrolled_window = Gtk3::ScrolledWindow->new();
$scrolled_window->set_border_width(5);
$scrolled_window->set_policy('automatic','automatic');
my $textview = Gtk3::TextView->new();
my $buffer = $textview->get_buffer();
$buffer->set_text ("Hello, this is some text\nHello world\n");
$textview->set_wrap_mode('none');
$textview->set_editable(FALSE);
$textview->set_cursor_visible(FALSE);
set_widget_property( $textview, 'font-size', '18px' );
my $bg_color = Gtk3::Gdk::RGBA::parse( "#411934" );
$textview->override_background_color('normal', $bg_color);
my $color = Gtk3::Gdk::RGBA::parse( "#e9e5e8" );
$textview->override_color('normal', $color);
$textview->set_monospace(TRUE);

$scrolled_window->add($textview);
$frame1->add($scrolled_window);
$window->set_border_width(5);
$window->set_default_size( 600, 400 );
$window->set_position('center_always');
$window->show_all();
setup_background_command( $buffer );  # start background command
my $condvar = AnyEvent->condvar;
$window->signal_connect( destroy  => sub { $condvar->send } );
my $done = $condvar->recv;  # enter main loop...

sub setup_background_command {
    my ( $buffer ) = @_;

    my $job = AnyEvent::Subprocess->new(
        delegates     => [ 'StandardHandles', 'CompletionCondvar' ],
        code          => sub { exec 'unbuffer', 'myscript.pl' }
    );
    my $run = $job->run;
    $run->delegate('stdout')->handle->on_read(
        sub {
            my ( $handle ) = @_;
            my $line = $handle->rbuf;
            chomp $line;
            my $iter = $buffer->get_end_iter();
            $buffer->insert( $iter, $line . "\n" );
            $handle->rbuf = ""; # clear buffer
        }
    );
}

sub set_widget_property {
    my ( $widget, $prop, $value ) = @_;

    my $context = $widget->get_style_context();
    my $cls_name = $prop . '_class';
    $context->add_class( $cls_name );
    my $provider = Gtk3::CssProvider->new();
    my $css = sprintf ".%s {%s: %s;}", $cls_name, $prop, $value;
    $provider->load_from_data( $css );
    $context->add_provider($provider, GTK_STYLE_PROVIDER_PRIORITY_USER);
}

Here, the command to run asynchronously within GTK event loop is the script myscript.pl:

#! /usr/bin/env perl
use feature qw(say);
use strict;
use warnings;

#STDOUT->autoflush(1);
sleep 1;
say "data 1";
sleep 1;
say "data 2";
sleep 1;
say "data 3";

Notice that the script can be made unbuffered by uncommenting the line with autoflush(1). But in general we must assume that we cannot modify the internals of the command, so I used unbuffer to run the script.
