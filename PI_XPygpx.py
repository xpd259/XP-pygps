import gpxpy
import gpxpy.gpx
from XPLMDataAccess import *
from XPLMDefs import *
from XPLMPlugin import *
from XPLMProcessing import *
from XPLMUtilities import *
from XPLMDisplay import *
from XPLMGraphics import *


class PythonInterface:
    def XPluginStart(self):
        global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl, gpx, gpx_track, gpx_segment
        self.Name = "Flight tracer"
        self.Sig = "Dick-Thomas.Python.X-Plane-Flight-Tracker"
        self.Desc = "Tracks Flight to a GPX file"
        self.Clicked = 0

        gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        ## open a file and write to it
        self.outputPath = XPLMGetSystemPath() + "flightsim.gpx"
        self.OutputFile = open(self.outputPath, 'w')

        """find the data refs we want to record"""
        self.PlaneLat = XPLMFindDataRef("sim/flightmodel/position/latitude")
        self.PlaneLon = XPLMFindDataRef("sim/flightmodel/position/longitude")
        self.PlaneEl = XPLMFindDataRef("sim/flightmodel/position/elevation")

        self.DrawWindowCB = self.DrawWindowCallback
        self.KeyCB = self.KeyCallback
        self.MouseClickCB = self.MouseClickCallback
        self.WindowId = XPLMCreateWindow(self, 50, 600, 300, 400, 1, self.DrawWindowCB, self.KeyCB, self.MouseClickCB,
                                         0)

        """
        Register our callback for every 5 seconds  Positive intervals
        are in seconds, negative are the negative of sim frames.  Zero
        registers but does not schedule a callback for time.
        """
        self.FlightLoopCB = self.FlightLoopCallback
        XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 5.0, 0)
        return self.Name, self.Sig, self.Desc

    def XPluginStop(self):
        XPLMDestroyWindow(self, self.WindowId)
        XPLMUnregisterFlightLoopCallback(self, self.FlightLoopCB, 0)

        self.OutputFile.write(gpx.to_xml())
        self.OutputFile.close()

        pass

    def XPluginEnable(self):
        return 1

    def XPluginDisable(self):
        pass

    def XPluginReceiveMessage(self, inFromWho, inMessage, inParam):
        pass

    def Update(self, inFlightLoopCallback, inInterval, inRelativeToNow, inRefcon):
        pass

    def FlightLoopCallback(self, elapsedMe, elapsedSim, counter, refcon):

        lat = XPLMGetDataf(self.PlaneLat)
        lon = XPLMGetDataf(self.PlaneLon)
        el = XPLMGetDataf(self.PlaneEl)

        """Write data to memory"""
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, el))

        """return in 5.0 seconds"""
        return 5.0

    def DrawWindowCallback(self, inWindowID, inRefcon):
        # First we get the location of the window passed in to us.
        lLeft = [];
        lTop = [];
        lRight = [];
        lBottom = []
        XPLMGetWindowGeometry(inWindowID, lLeft, lTop, lRight, lBottom)
        left = int(lLeft[0]);
        top = int(lTop[0]);
        right = int(lRight[0]);
        bottom = int(lBottom[0])
        """
        We now use an XPLMGraphics routine to draw a translucent dark
        rectangle that is our window's shape.
        """
        gResult = XPLMDrawTranslucentDarkBox(left, top, right, bottom)
        color = 1.0, 1.0, 1.0

        if self.Clicked:
            Desc = "I'm a plugin 1"
        else:
            Desc = "Hello World 1"

        """
        Finally we draw the text into the window, also using XPLMGraphics
        routines.  The NULL indicates no word wrapping.
        """
        gResult = XPLMDrawString(color, left + 5, top - 20, Desc, 0, xplmFont_Basic)
        pass

    def KeyCallback(self, inWindowID, inKey, inFlags, inVirtualKey, inRefcon, losingFocus):
        pass

    """
    MyHandleMouseClickCallback

    Our mouse click callback toggles the status of our mouse variable
    as the mouse is clicked.  We then update our text on the next sim
    cycle.
    """

    def MouseClickCallback(self, inWindowID, x, y, inMouse, inRefcon):
        """
        If we get a down or up, toggle our status click.  We will
        never get a down without an up if we accept the down.
        """
        if ((inMouse == xplm_MouseDown) or (inMouse == xplm_MouseUp)):
            self.Clicked = 1 - self.Clicked

        """
        Returning 1 tells X-Plane that we 'accepted' the click; otherwise
        it would be passed to the next window behind us.  If we accept
        the click we get mouse moved and mouse up callbacks, if we don't
        we do not get any more callbacks.  It is worth noting that we
        will receive mouse moved and mouse up even if the mouse is dragged
        out of our window's box as long as the click started in our window's
        box.
        """
        return 1
