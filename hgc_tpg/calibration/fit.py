import ROOT 
import os,sys, math,re

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetOptTitle(0)

## TODO: make configurable (CONF)

## fit and write down parameters
name = "rawt_layer_%d_truept_%.0f" ## CONF
outname="calibration_fit.txt" ## CONF
inname="calibration.root"

rebin=10 ##DEFAULT
layers=range(1,30) ## CONF
truth=[5.,10.,30.,50.,100.,500.,1000.] ## CONF
xmin,xmax=0,10000

ranges={
        #rawt
        ## layer -> [[etmin,etmax), (rebin,xmin,xmax)]
        1 : [ [0,8000,1,200,1000]  ],
        2 : [ [0, 30,1,200,1000], [ 30,100,1,200,5000], [100,8000,1,400,5000]  ],
        3 : [ [0, 50,1,200,5000], [ 50,100,10,1000,10000] , [100,8000,10,1500,30000] ],
        4 : [ [0, 30,2,200,2000], [ 30,500,10,800,10000], [500,8000,100,1500,30000]  ],###
        5 : [ [0, 10,1,250,2000], [ 10,500,10,1000,10000], [500,8000,100,1500,30000] ],
        6 : [ [0, 10,1,250,2000], [ 10,500,10,1000,10000], [500,8000,100,1500,30000]  ],
        ###
        7 : [ [0, 10,1,250,2000], [ 10,100,10,1000,10000], [100,8000,100,1500,30000]  ],
        8 : [ [0, 10,1,250,2000], [ 10,50,10,1000,10000],  [50,8000,100,5000,100000]  ],
        9 : [ [0, 10,1,250,2000], [ 10, 50,10,1000,10000], [30,100,30,2000,30000], [100,8000,100,5000,100000]  ],
        10: [ [0, 10,1,250,2000], [ 10, 50,10,1000,10000], [30,100,30,2000,30000], [100,8000,100,5000,100000]  ],
        11: [ [0, 10,1,250,2000], [ 10, 30,10,1000,10000], [30,100,30,2000,30000], [100,8000,100,5000,100000]  ],
        12: [ [0, 10,1,250,2000], [ 10, 50,10,1000,10000], [30,500,30,2000,30000], [500,8000,100,5000,100000]  ],
        13: [ [0, 10,1,250,2000], [ 10, 50,10,1000,10000], [30,500,30,2000,30000], [500,8000,100,5000,100000]  ],
        14: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        15: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        16: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        17: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        18: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        19: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        20: [ [0, 30,1,250,2000], [ 30,100,10,1000,10000], [100,8000,100,15000,100000]  ],
        ###
        20: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        21: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        22: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        23: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        24: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        25: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        26: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        27: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        28: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        29: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        30: [ [0, 30,1,250,2000], [ 30,500,10,1000,10000], [500,8000,100,15000,100000]  ],
        }

###
fIn=ROOT.TFile.Open(inname) 

out = open(outname,"w")
print >> out, "## ETtruth LAYER FUNC MVP SIGMA"
fOut=ROOT.TFile.Open(re.sub('.txt','.root',outname),"RECREATE" )

f=ROOT.TF1("myfunc","[0]*TMath::Landau(x,[1],[2],1)",xmin,xmax)
f2=ROOT.TF1("myfunc2","[0]*TMath::Gaus(x,[1],[2])",xmin,xmax)
print >>sys.stderr, "-> Setting Minuit2"
ROOT.Math.MinimizerOptions.SetDefaultMinimizer("Minuit2")

graphs={}

for il in layers:
   graphs["mpv_layer%d"%il] = ROOT.TGraph()
   graphs["mpv_layer%d"%il] . SetName("mpv_layer%d"%il) 
   graphs["mpv_layer%d"%il] . SetMarkerStyle(21)
   graphs["mpv_layer%d"%il] . SetMarkerSize(0.05)

   graphs["sigma_layer%d"%il] = ROOT.TGraph()
   graphs["sigma_layer%d"%il].SetName("sigma_layer%d"%il) 
   graphs["sigma_layer%d"%il] . SetMarkerColor(ROOT.kRed)
   graphs["sigma_layer%d"%il] . SetMarkerStyle(22)
   graphs["sigma_layer%d"%il] . SetMarkerSize(0.05)

   range_list=None
   if il in ranges: range_list=ranges[il]

   mean_max=0.0
   for pt in truth:
      ##
      h= fIn.Get(name%(il,pt) )
      if h==None:
          print >>sys.stderr, "Unable to fetch histogram",name%(il,pt)
          continue
      fitmin,fitmax=xmin,xmax
      fitrebin=rebin
      if range_list!=None:
          for etmin, etmax, rrebin, rmin ,rmax  in range_list:
              if pt >= etmin and pt<etmax:
                  fitmin = rmin
                  fitmax = rmax
                  fitrebin= rrebin
      fitmin = max(h.GetBinLowEdge(1), fitmin)
      fitmax = min(h.GetBinLowEdge(h.GetNbinsX()+1)-0.1, fitmax)
      f.SetRange(fitmin,fitmax)
      ##
         
      h.Rebin(fitrebin)

      c = ROOT.TCanvas("c","c",100,100)
      h.Draw("PE")
      h.GetXaxis().SetRangeUser(fitmin*.8,fitmax*1.2)

      fitok=True
    
      maxbin=0.0
      for ib in range(h.FindBin(fitmin),h.FindBin(fitmax)):
          if maxbin< h.GetBinContent(ib):
              maxbin=h.GetBinContent(ib)
              mpv0 = h.GetBinCenter(ib)

      rms0=0.0
      den=0.0
      for ib in range(h.FindBin(fitmin),h.FindBin(fitmax)):
          rms0+=(h.GetBinCenter(ib) - mpv0)**2 * h.GetBinContent(ib)
          den+=h.GetBinContent(ib)
      rms0 = math.sqrt(rms0/den)

      rms1=0.0
      den=0.0
      for ib in range(h.FindBin(mpv0*.5),h.FindBin(mpv0*1.5)):
          rms1+=(h.GetBinCenter(ib) - mpv0)**2 * h.GetBinContent(ib)
          den+=h.GetBinContent(ib)
      rms1 = math.sqrt(rms1/den)

      print "DEUBG: layer=",il,"mpv=",mpv0,"rms0=",rms0,"rms1=",rms1

      fitok=False

      ## if True: ## try Laundau 
      ##   f.SetParameter(0,h.Integral(h.FindBin(fitmin),h.FindBin(fitmax)))
      ##   f.SetParameter(1,mpv0)
      ##   f.SetParameter(2,rms0)
      ##   f.SetLineColor(ROOT.kBlue)
      ##   r = h.Fit("myfunc","W L I S R N")
      ##   fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
      ##   ## reset pars
      ##   c.SetFillColor(ROOT.kCyan)
      ##   print >>out,"%.0f %d L %.1f %.1f" %(pt,il,f.GetParameter(1),f.GetParameter(2))
      ##   if fitok: 
      ##       c.SetFillColor(ROOT.kCyan-10)
      ##       f.SetLineStyle(1)
      ##       f.SetLineWidth(2)
      ##       f.Draw("L SAME")
      ##   else : 
      ##       f.SetLineStyle(7)
      ##       f.SetLineWidth(1)
      ##       f.Draw("L SAME")

      if not fitok:  ## first fit  USE RMS1, bounded by fitmin,fitmax
        f2.SetParameter(0,h.Integral( h.FindBin(max(mpv0-2*rms1,fitmin)),h.FindBin(min(mpv0+2*rms1,fitmax))))
        f2.SetParameter(1,mpv0)
        f2.SetParameter(2,rms1)
        f2.SetRange(mpv0-2*rms1,mpv0+2*rms1)
        r = h.Fit("myfunc2","W L I S R N")
        try:
            fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
        except ZeroDivisionError:
            fitok=False
        if fitok: 
            f2.SetLineStyle(1)
            f2.SetLineWidth(2)
            f2.Draw("L SAME")
            c.SetFillColor(ROOT.kGreen-10)
        else : 
            f2.SetLineStyle(7)
            f2.SetLineWidth(1)
            f2.Draw("L SAME")

      if not fitok:  ## first fit / within 2sigma
        f2.SetParameter(0,h.Integral( h.FindBin(max(mpv0-2*rms0,fitmin)),h.FindBin(min(mpv0+2*rms0,fitmax))))
        #f2.SetParameter(0,h.Integral( h.FindBin(mpv0-2*rms0),h.FindBin(mpv0+2*rms0)))
        f2.SetParameter(1,mpv0)
        f2.SetParameter(2,rms0)
        f2.SetRange(mpv0-2*rms0,mpv0+2*rms0)
        r = h.Fit("myfunc2","W L I S R N")
        fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
        if fitok: 
            f2.SetLineStyle(1)
            f2.SetLineWidth(2)
            f2.Draw("L SAME")
        else : 
            f2.SetLineStyle(7)
            f2.SetLineWidth(1)
            f2.Draw("L SAME")



      if not fitok: ## change range -- all range
        f2.SetParameter(0,h.Integral(h.FindBin(fitmin),h.FindBin(fitmax)))
        f2.SetParameter(1,mpv0)
        f2.SetParameter(2,rms0)
        f2.SetRange(fitmin,fitmax)

        r = h.Fit("myfunc2","W L I S R N")
        fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
        if fitok: 
            f2.SetLineStyle(1)
            f2.SetLineWidth(2)
            c.SetFillColor(ROOT.kGray)
            f2.Draw("L SAME")
        else : 
            f2.SetLineStyle(7)
            f2.SetLineWidth(1)
            f2.Draw("L SAME")

      if not fitok: ## try to refit with a gaus and -1.5, 3 sigma range
        f2.SetParameter(0,h.Integral(h.FindBin(fitmin),h.FindBin(fitmax)))
        f2.SetParameter(1,mpv0)
        f2.SetParameter(2,rms0)
        f2.SetRange(mpv0-1.5*rms0,mpv0+2.0*rms0)

        r = h.Fit("myfunc2","W L I S R N")
        fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
        if fitok: 
            f2.SetLineStyle(1)
            f2.SetLineWidth(2)
            f2.Draw("L SAME")
        else : 
            f2.SetLineStyle(7)
            f2.SetLineWidth(1)
            f2.Draw("L SAME")

      if not fitok: ## try to refit with a gaus and -1.5, 3 sigma range
        f2.SetParameter(0,h.Integral(h.FindBin(fitmin),h.FindBin(fitmax)))
        f2.SetParameter(1,mpv0)
        f2.SetParameter(2,rms0)
        f2.SetRange(mpv0-1*rms0,mpv0+1*rms0)

        r = h.Fit("myfunc2","W L I S R N")
        fitok = ( r.Status() == 0 and r.Chi2()/r.Ndf() < 10)
        if fitok: 
            f2.SetLineStyle(1)
            f2.SetLineWidth(2)
            f2.Draw("L SAME")
            c.SetFillColor(ROOT.kGray)
        else : 
            f2.SetLineStyle(7)
            f2.SetLineWidth(1)
            f2.Draw("L SAME")


      if r.Chi2()/r.Ndf() >=10.:
          c.SetFillColor(ROOT.kOrange)
      if r.Status() != 0:
          c.SetFillColor(ROOT.kYellow)

      ltx=ROOT.TLatex()
      ltx.SetNDC()
      ltx.SetTextFont(42)
      ltx.SetTextSize(0.03)
      ltx.SetTextAlign(11)
      ltx.DrawLatex(0.7,.85,"mpv0=%.0f"%mpv0)
      ltx.DrawLatex(0.7,.80,"rms0=%.0f"%rms0)
      ltx.DrawLatex(0.7,.75,"chi2/ndf=%.1f"% (r.Chi2()/r.Ndf()))
      ltx.DrawLatex(0.7,.70,"status=%d"%r.Status())
      ltx.DrawLatex(0.7,.65,"mean (fit)=%.0f"%f2.GetParameter(1))
      ltx.DrawLatex(0.7,.60,"sigma=%.0f"%f2.GetParameter(2))

      cname = "plot/calibration/fit_layer_%d_truept_%.0f.pdf" ## CONF
      c.SaveAs(cname%(il,pt))
      graphs["mpv_layer%d"%il].SetPoint( graphs["mpv_layer%d"%il].GetN(), pt, f2.GetParameter(1))
      graphs["sigma_layer%d"%il].SetPoint( graphs["sigma_layer%d"%il].GetN(), pt, f2.GetParameter(2))
      print >>out,"%.0f %d G %.1f %.1f" %(pt,il,f2.GetParameter(1),f2.GetParameter(2))
      mean_max = max(mean_max,f2.GetParameter(1))

   c = ROOT.TCanvas("c","c",100,100)
   dummy=ROOT.TH1D("dummy","dummy",1000,0,1000)
   dummy.Draw("AXIS")
   dummy.GetXaxis().SetTitle("p_{T}^{truth}[GeV]")
   dummy.GetYaxis().SetRangeUser(0,mean_max*1.3)
   graphs["mpv_layer%d"%il] . Draw("P SAME")
   graphs["sigma_layer%d"%il] . Draw("P SAME")
   cname = "plot/calibration/params_layer_%d.pdf" ## CONF
   c.SaveAs(cname%(il))

   fOut.cd()
   graphs["mpv_layer%d"%il] . Write()
   graphs["sigma_layer%d"%il] . Write()

fOut.Close()
print >>sys.stderr,"-> Done"


