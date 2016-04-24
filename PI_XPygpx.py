import time

import gpxpy
import gpxpy.gpx
from XPLMDataAccess import *
from XPLMDefs import *
from XPLMDisplay import *
from XPLMGraphics import *
from XPLMPlugin import *
from XPLMProcessing import *
from XPLMUtilities import *
from XPWidgetDefs import *


class PythonInterface:
    def XPluginStart(self):
        global gOutputFile, gPlaneLat, gPlaneLon, gPlaneEl, gpx, gpx_track, gpx_segment
        self.Name = "Flight tracer"
        self.Sig = "DickThomas.XPGPS"
        self.Desc = "Tracks Flight to a GPX file"
        dateNow = time.strftime("%Y%m%d-%H%M%S")

        # Create first track in our GPX
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)

        # Create first segment in our GPX track:
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        ## open a file and write to it
        self.outputPath = XPLMGetSystemPath() + "flightsim-" + dateNow + ".gpx"
        self.OutputFile = open(self.outputPath, 'w')

        """find the data refs we want to record"""
        self.PlaneLat = XPLMFindDataRef("sim/flightmodel/position/latitude")
        self.PlaneLon = XPLMFindDataRef("sim/flightmodel/position/longitude")
        self.PlaneEl = XPLMFindDataRef("sim/flightmodel/position/elevation")


        self.FlightLoopCB = self.FlightLoopCallback
        XPLMRegisterFlightLoopCallback(self, self.FlightLoopCB, 120.0, 0)
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
        el = XPLMGetDataf(self.PlaneEl)

        """Write data to memory"""
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, el))
        """return in 120.0 seconds"""
        return 120.0
