import gpxpy
import gpxpy.gpx
from XPLMDataAccess import *
from XPLMDefs import *
from XPLMPlugin import *
from XPLMProcessing import *
from XPLMUtilities import *

class PythonInterface:
    def XPluginStart(self):
        global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl, gpx, gpx_track, gpx_segment
        self.Name = "Flight tracer XP-pygps"
        self.Sig = "Dick-Thomas.Python.X-Plane-Flight-Tracker"
        self.Desc = "Tracks Flight to a GPX file"

        gpx = gpxpy.gpx.GPX()
        # Create first track in our GPX:
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        ## open a file and write to it
        self.outputPath = XPLMGetSystemPath() + "flightsim.gpx"
        self.OutputFile = open(self.outputPath, 'w')

        ## find the data refs we are seeking
        self.PlaneLat = XPLMFindDataRef("sim/flightmodel/position/latitude")
        self.PlaneLon = XPLMFindDataRef("sim/flightmodel/position/longitude")
        self.PlaneEl = XPLMFindDataRef("sim/flightmodel/position/elevation")

        """
        Register our callback for every 5 seconds  Positive intervals
        are in seconds, negative are the negative of sim frames.  Zero
        registers but does not schedule a callback for time.
        """
        self.FlightLoopCB = self.FlightLoopCallback
        XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 5.0, 0)
        return self.Name, self.Sig, self.Desc


    def XPluginStop(self):
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
        el =  XPLMGetDataf(self.planeEl)
        """Write data to memory"""
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, el))

        """return in 5.0 seconds"""
        return 5.0
