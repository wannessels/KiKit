from pcbnewTransition import pcbnew
import os
import shutil
from pathlib import Path
from kikit.export import gerberImpl, exportSettingsOSHPark, fullGerberPlotPlan, LayerToPlot
from kikit.fab.common import ensurePassingDrc

plotPlanNoVCuts = [layer_to_plot for layer_to_plot in fullGerberPlotPlan if layer_to_plot is not LayerToPlot.CmtUser]

def exportOSHPark(board, outputdir, nametemplate, drc):
    """
    Prepare fabrication files for OSH Park
    """
    loadedBoard = pcbnew.LoadBoard(board)
    Path(outputdir).mkdir(parents=True, exist_ok=True)

    if drc:
        ensurePassingDrc(loadedBoard)

    gerberdir = os.path.join(outputdir, "gerber")
    shutil.rmtree(gerberdir, ignore_errors=True)
    gerberImpl(board, gerberdir, plot_plan=plotPlanNoVCuts, settings=exportSettingsOSHPark)
    archiveName = nametemplate.format("gerbers")
    shutil.make_archive(os.path.join(outputdir, archiveName), "zip", outputdir, "gerber")
