"""
    Base class for reports. Child classes will need to implement
    the onSave() method.
"""
import wx
import logging
import sys
import wx.html as html

logger = logging.getLogger(__name__)

ISPDF = False
if sys.platform == "win32":
    _STATICBOX_WIDTH = 450
    PANEL_WIDTH = 500
    PANEL_HEIGHT = 700
    FONT_VARIANT = 0
    ISPDF = True
# For OSX and everything else
else:
    _STATICBOX_WIDTH = 480
    PANEL_WIDTH = 530
    PANEL_HEIGHT = 700
    FONT_VARIANT = 1
    ISPDF = True

class BaseReportDialog(wx.Dialog):

    def __init__(self, report_list, *args, **kwds):
        """
        Initialization. The parameters added to Dialog are:

        :param report_list: list of html_str, text_str, image for report
        """
        kwds["style"] = wx.RESIZE_BORDER|wx.DEFAULT_DIALOG_STYLE
        super(BaseReportDialog, self).__init__(*args, **kwds)
        kwds["image"] = 'Dynamic Image'

        # title
        self.SetTitle("Report")
        # size
        self.SetSize((720, 650))
        # font size
        self.SetWindowVariant(variant=FONT_VARIANT)
        # check if tit is MAC
        self.is_pdf = ISPDF
        # report string
        self.report_list = report_list
        # wild card
        if self.is_pdf:  # pdf writer is available
            self.wild_card = 'PDF files (*.pdf)|*.pdf|'
            self.index_offset = 0
        else:
            self.wild_card = ''
            self.index_offset = 1
        self.wild_card += 'HTML files (*.html)|*.html|'
        self.wild_card += 'Text files (*.txt)|*.txt'

    def _setup_layout(self):
        """
        Set up layout
        """
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        # buttons
        button_close = wx.Button(self, wx.ID_OK, "Close")
        button_close.SetToolTipString("Close this report window.")
        hbox.Add(button_close)
        button_close.SetFocus()

        button_print = wx.Button(self, wx.NewId(), "Print")
        button_print.SetToolTipString("Print this report.")
        button_print.Bind(wx.EVT_BUTTON, self.onPrint,
                          id=button_print.GetId())
        hbox.Add(button_print)

        button_save = wx.Button(self, wx.NewId(), "Save")
        button_save.SetToolTipString("Save this report.")
        button_save.Bind(wx.EVT_BUTTON, self.onSave, id=button_save.GetId())
        hbox.Add(button_save)

        # panel for report page
        vbox = wx.BoxSizer(wx.VERTICAL)
        # html window
        self.hwindow = html.HtmlWindow(self, style=wx.BORDER)
        # set the html page with the report string
        self.hwindow.SetPage(self.report_html)

        # add panels to boxsizers
        vbox.Add(hbox)
        vbox.Add(self.hwindow, 1, wx.EXPAND|wx.ALL,0)

        self.SetSizer(vbox)
        self.Centre()
        self.Show(True)

    def onPreview(self, event=None):
        """
        Preview
        : event: Preview button event
        """
        previewh = html.HtmlEasyPrinting(name="Printing", parentWindow=self)
        previewh.PreviewText(self.report_html)

    def onPrint(self, event=None):
        """
        Print
        : event: Print button event
        """
        printh = html.HtmlEasyPrinting(name="Printing", parentWindow=self)
        printh.PrintText(self.report_html)

    def OnClose(self, event=None):
        """
        Close the Dialog
        : event: Close button event
        """
        self.Close()

    def HTML2PDF(self, data, filename):
        """
        Create a PDF file from html source string.
        Returns True is the file creation was successful.
        : data: html string
        : filename: name of file to be saved
        """
        #try:
        from xhtml2pdf import pisa
        # open output file for writing (truncated binary)
        resultFile = open(filename, "w+b")
        # convert HTML to PDF
        data = '<html><head><meta http-equiv=Content-Type content=\'text/html; charset=windows-1252\'><meta name=Generator ></head><body lang=EN-US>' \
               '<div class=WordSection1><p class=MsoNormal><b><span ><center><font size=\'4\' >cyl_400_40.txt [Feb 26 2018 12:04:42]</font></center></span></center></b></p><p class=MsoNormal>&nbsp;</p>' \
               '<p class=MsoNormal><center><font size=\'4\' > File name:/Volumes/SasView-4.2.0-MacOSX/SasView 4.2.0.app/Contents/Resources/test/1d_data/cyl_400_40.txt</font></center></p>' \
               '<p class=MsoNormal><center><font size=\'4\' > Model name:cylinder </font></center></p>' \
               '<p class=MsoNormal><center><font size=\'4\' > Q Range:    min =  0.00925926, max =  0.5 </font></center></p>' \
               '<p class=MsoNormal><center><font size=\'4\' > Chi2/Npts = 21178 </font></center></p><p class=MsoNormal>&nbsp;</p>' \
               '<p class=MsoNormal><center><font size=\'4\' > scale = 1 +- (fixed)</font></center></p><p class=MsoNormal><center><font size=\'4\' > background = 0.001 +- (fixed) 1/cm </font>' \
               '</center></p><p class=MsoNormal><center><font size=\'4\' > sld = 4 +- (fixed) 1e-6/Ang^2</font></center></p><p class=MsoNormal><center><font size=\'4\' > sld_solvent = 1 +- (fixed) 1e-6/Ang^2' \
               '</font></center></p><p class=MsoNormal><center><font size=\'4\' > radius = 20 +- (fixed) Ang </font></center></p><p class=MsoNormal><center><font size=\'4\' > length = 400 +- (fixed) Ang</font></center></p>' \
               '<p class=MsoNormal>&nbsp;</p><p class=MsoNormal>&nbsp;</p><br><p class=MsoNormal><b><span ><center> <font size=\'4\' > Graph</font></span></center></b></p>' \
               '<p class=MsoNormal>&nbsp;</p><center><br><font size=\'4\' >Model Computation</font><br><font size=\'4\' >Data: "cyl_400_40.txt [Feb 26 2018 12:04:42]"</font><br>' \
               '<img src="/Users/wojciechpotrzebowski/Desktop/sasview_reporting2_img0.png" ></img><p class=MsoNormal>&nbsp;</p><img src="/Users/wojciechpotrzebowski/Desktop/sasview_reporting2_img1.png" ></img>'
        pisaStatus = pisa.CreatePDF(data, dest=resultFile)
        # close output file
        resultFile.close()
        self.Update()
        #    return pisaStatus.err
        #except Exception:
        #    logger.error("Error creating pdf: %s" % sys.exc_value)
        logger.error("Error creating pdf: %s" % pisaStatus.err)
        return False
