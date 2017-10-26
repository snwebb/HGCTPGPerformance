import ROOT
import numpy as np
import sys,os
from array import array

#qcd_flat_nopu.root  
#qcd_flat_pu140.root  
#qcd_flat_pu200.root  

obj=[]

def draw_canvas(name="c"):
    c=ROOT.TCanvas(name,name,800,800)
    c.SetTopMargin(0.05)
    c.SetRightMargin(0.05)
    c.SetBottomMargin(0.15)
    c.SetLeftMargin(0.15)
    obj.append(c)
    return c

def draw_text():
    t=ROOT.TLatex()
    t.SetNDC()
    t.SetTextFont(43)
    t.SetTextSize(28)
    t.SetTextAlign(13)
    t.DrawLatex(.18,.92,"#bf{HGCAL} #scale[0.8]{#it{Simulation}}")
    obj.append(t)
    return t

def draw_line():
    g=ROOT.TGraph()
    g.SetName("g1")
    g.SetPoint(0,0,1)
    g.SetPoint(1,1000,1)
    g.SetLineColor(ROOT.kGray+1)
    g.SetLineWidth(2)
    g.SetLineStyle(7)
    g.Draw("L SAME")
    obj.append(g)
    return g

def plot_turnon(ftype="nopu"):
    files={ "nopu":ROOT.TFile.Open("qcd_flat_nopu.root"),
            "pu140":ROOT.TFile.Open("qcd_flat_pu140.root"),
            "pu200":ROOT.TFile.Open("qcd_flat_pu200.root")
            }
    ##
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ## turn on -- no pu
    c=draw_canvas("turnon_pt")
    rebin=array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,250,300,350,400,450,500,600,700,800,1000])
    
    histos={}
    x,y=.7,.19
    leg = ROOT.TLegend(x,y,x+.22,y+.20)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(None,"   1.5 < |#eta_{j}| < 3.0","h")

    #for pt,col in zip([35,80,120,500],[ROOT.kGreen-2,38,46,ROOT.kOrange-4]):
    for pt,col in zip([50,100,150,200],[ROOT.kGreen-2,38,46,ROOT.kOrange-4]):
    #for pt,col in zip([35,80,120],[ROOT.kGreen-2,38,46]):
        # get
        histos["pt%d_num"%pt] = files[ftype] . Get("turnon_pt%d_num"%pt)
        histos["pt%d_den"%pt] = files[ftype] . Get("turnon_pt%d_den"%pt)
        if histos["pt%d_num"%pt] == None: print "<*> ERROR: unable to get:","turnon_pt%d_num"%pt
        if histos["pt%d_den"%pt] == None: print "<*> ERROR: unable to get:","turnon_pt%d_den"%pt
        # rebin
        histos["pt%d_num"%pt] = histos["pt%d_num"%pt] . Rebin(len(rebin)-1,"pt%d_num_rebin"%pt,rebin)
        histos["pt%d_den"%pt] = histos["pt%d_den"%pt] . Rebin(len(rebin)-1,"pt%d_den_rebin"%pt,rebin)
        # divide
        histos["pt%d"%pt] =  histos["pt%d_num"%pt].Clone("pt%d_turnon"%pt)
        histos["pt%d"%pt] . Divide(histos["pt%d_den"%pt])

        histos["pt%d"%pt] . SetLineWidth(2)
        histos["pt%d"%pt] . SetLineColor(col)
        leg.AddEntry(histos["pt%d"%pt],"p_{T}^{raw} > %d GeV"%pt,"L")

        if pt==50:
            histos["pt%d"%pt] . GetXaxis() . SetTitle("p_{T}^{gen} [GeV]")
            histos["pt%d"%pt] . GetYaxis() . SetTitle("#varepsilon")
            histos["pt%d"%pt] . GetXaxis() . SetTitleOffset(1.5)
            histos["pt%d"%pt] . GetYaxis() . SetTitleOffset(1.5)
            histos["pt%d"%pt] . GetYaxis() . SetRangeUser(0,1.1)
            histos["pt%d"%pt] . GetXaxis() . SetRangeUser(0,500)
            histos["pt%d"%pt] . Draw("AXIS")
            draw_line()
            histos["pt%d"%pt] . Draw("AXIS X+ Y+ SAME")
            histos["pt%d"%pt] . Draw("AXIS SAME")

        histos["pt%d"%pt] . Draw(" HIST SAME")

    histos["pt%d"%50] . Draw("AXIS X+ Y+ SAME")
    histos["pt%d"%50] . Draw("AXIS SAME")

    draw_text()
    leg.Draw("SAME")
    c.Modified()
    c.Update()
    raw_input("ok?")
    c.SaveAs("plot/turnon_pt_"+ftype+".pdf")

def plot_turnon_pu():
    doFit=True
    files={ "nopu":ROOT.TFile.Open("qcd_flat_nopu.root"),
            "pu140":ROOT.TFile.Open("qcd_flat_pu140.root"),
            "pu200":ROOT.TFile.Open("qcd_flat_pu200.root")
            }
    ##
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ## turn on -- no pu
    c=draw_canvas("turnon_pt")
    #rebin=array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,140,160,180,200,250,300,350,400,450,500,600,700,800,1000])
    rebin=array('d',[0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,300,350,400,450,500,600,700,800,1000])
    
    histos={}
    x,y=.6,.20
    leg = ROOT.TLegend(x,y,x+.3,y+.25)
    leg.SetFillStyle(0)
    leg.SetBorderSize(0)
    leg.AddEntry(None,"   1.5 < |#eta_{j}| < 3.0","h")
    pt=150
    
    #print "No 140"
    fitFunc={}
    for pu,col in zip([0,140,200],[ROOT.kGreen-2,38,46]):
    #for pu,col in zip([0,200],[ROOT.kGreen-2,38,46]):
    #for pt,col in zip([35,80,120],[ROOT.kGreen-2,38,46]):
        # get
        if pu==0:
            histos["pt%d_pu%d_num"%(pt,pu)] = files["nopu"] . Get("turnon_pt%d_num"%pt)
            histos["pt%d_pu%d_den"%(pt,pu)] = files["nopu"] . Get("turnon_pt%d_den"%pt)
        else:
            histos["pt%d_pu%d_num"%(pt,pu)] = files["pu%d"%pu] . Get("turnon_pt%d_num"%pt)
            histos["pt%d_pu%d_den"%(pt,pu)] = files["pu%d"%pu] . Get("turnon_pt%d_den"%pt)

        # rebin
        histos["pt%d_pu%d_num"%(pt,pu)] = histos["pt%d_pu%d_num"%(pt,pu)] . Rebin(len(rebin)-1,"pt%d_pu%d_num_rebin"%(pt,pu),rebin)
        histos["pt%d_pu%d_den"%(pt,pu)] = histos["pt%d_pu%d_den"%(pt,pu)] . Rebin(len(rebin)-1,"pt%d_pu%d_den_rebin"%(pt,pu),rebin)
        # divide
        histos["pt%d_pu%d"%(pt,pu)] =  histos["pt%d_pu%d_num"%(pt,pu)].Clone("pt%d_pu%d_turnon"%(pt,pu))
        histos["pt%d_pu%d"%(pt,pu)] . Divide(histos["pt%d_pu%d_den"%(pt,pu)])

        histos["pt%d_pu%d"%(pt,pu)] . SetLineWidth(2)
        histos["pt%d_pu%d"%(pt,pu)] . SetLineColor(col)
        leg.AddEntry(histos["pt%d_pu%d"%(pt,pu)],"p_{T}^{raw} > %d GeV PU=%d"%(pt,pu),"L")

        if pu==0:
            histos["pt%d_pu%d"%(pt,pu)] . GetXaxis() . SetTitle("p_{T}^{gen} [GeV]")
            histos["pt%d_pu%d"%(pt,pu)] . GetYaxis() . SetTitle("#varepsilon")
            histos["pt%d_pu%d"%(pt,pu)] . GetXaxis() . SetTitleOffset(1.5)
            histos["pt%d_pu%d"%(pt,pu)] . GetYaxis() . SetTitleOffset(1.5)
            histos["pt%d_pu%d"%(pt,pu)] . GetYaxis() . SetRangeUser(0,1.1)
            histos["pt%d_pu%d"%(pt,pu)] . GetXaxis() . SetRangeUser(0,400)
            histos["pt%d_pu%d"%(pt,pu)] . Draw("AXIS")
            draw_line()
            histos["pt%d_pu%d"%(pt,pu)] . Draw("AXIS X+ Y+ SAME")
            histos["pt%d_pu%d"%(pt,pu)] . Draw("AXIS SAME")

        histos["pt%d_pu%d"%(pt,pu)] . Draw(" HIST SAME")
        if doFit:
            f = ROOT.TF1("func_pt%d_pu%d"%(pt,pu),"0.5*TMath::Erf( (x-[0])/[1]) +0.5",0,1000)
            f.SetParameter(0,pt)
            f.SetParameter(1,30)
            histos["pt%d_pu%d"%(pt,pu)].Fit("func_pt%d_pu%d"%(pt,pu),"WWNQ")
            f.SetLineColor(col)
            f.SetLineWidth(1)
            fitFunc[ "pt%d_pu%d"%(pt,pu)] = f
            f.Draw("L SAME")

    histos["pt%d_pu%d"%(pt,0)] . Draw("AXIS X+ Y+ SAME")
    histos["pt%d_pu%d"%(pt,0)] . Draw("AXIS SAME")

    draw_text()
    leg.Draw("SAME")
    c.Modified()
    c.Update()
    raw_input("ok?")
    c.SaveAs("plot/turnon_pu.pdf")

def plot_resolution(prefix="",ftype="nopu"):

    files={ "nopu":ROOT.TFile.Open("qcd_flat_nopu.root"),
            "pu140":ROOT.TFile.Open("qcd_flat_pu140.root"),
            "pu200":ROOT.TFile.Open("qcd_flat_pu200.root")
            }
    ##
    ROOT.gStyle.SetOptStat(0)
    ROOT.gStyle.SetOptTitle(0)
    ## turn on -- no pu
    c0=draw_canvas("fits")
    c0.Divide(4,4)

    #  KEY: TH1D res_pt30_40;1   res. pt 30 40
    #  KEY: TH1D res_pt40_50;1   res. pt 40 50
    #  KEY: TH1D res_pt50_60;1   res. pt 50 60
    #  KEY: TH1D res_pt60_70;1   res. pt 60 70
    #  KEY: TH1D res_pt70_80;1   res. pt 70 80
    #  KEY: TH1D res_pt80_90;1   res. pt 80 90
    #  KEY: TH1D res_pt90_100;1  res. pt 90 100
    #  KEY: TH1D res_pt100_120;1 res. pt 100 120
    #  KEY: TH1D res_pt120_150;1 res. pt 120 150
    #  KEY: TH1D res_pt150_200;1 res. pt 150 200
    #  KEY: TH1D res_pt200_300;1 res. pt 200 300
    #  KEY: TH1D res_pt300_500;1 res. pt 300 500
    #  KEY: TH1D res_pt500_1000;1    res. pt 500 1000
    #  KEY: TH1D res_pt1000_2000;1   res. pt 1000 2000
    #  KEY: TH1D res_pt2000_3000;1   res. pt 2000 3000 -> EMPTY
    
    histos={}
    fits={} ## store mu and sigma of a gaussian for a particular plot
    pt=80
    
    ptbins=[30,40,50,60,70,80,90,100,120,150,200,300,500,1000,2000]
    
    cIdx=1
    for idx, pt in enumerate(ptbins):
        if idx==len(ptbins)-1: continue
        c0.cd(cIdx)
        cIdx+=1
        pt2=ptbins[idx+1]
        histos["res_pt%d_%d"%(pt,pt2)] = files[ftype] . Get(prefix+"res_pt%d_%d"%(pt,pt2))
        h=histos["res_pt%d_%d"%(pt,pt2)]
        func=ROOT.TF1("myfunc","gaus",-5,5)
        func . SetParameter(0, h.Integral() )
        func . SetParameter(1, h.GetMean() )
        func . SetParameter(2, h.GetRMS() )
        m,s=h.GetMean(),h.GetRMS()
        func . SetRange( m-3*s , m+3*s)
        h . Fit ( "myfunc","LR")
        m,s= func.GetParameter(1),func.GetParameter(2)
        func . SetRange( m-3*s , m+3*s)
        h . Fit ( "myfunc","LR")
        m,s= func.GetParameter(1),func.GetParameter(2)
        func . SetRange( m-2*s , m+2*s)
        h . Fit ( "myfunc","LR")
        m,s= func.GetParameter(1),func.GetParameter(2)
        fits[ "res_pt%d_%d"%(pt,pt2)] = (m,s)
        
        obj.extend( [h,func] )
        h.Draw("H")
        func.Draw("F SAME")

    lin=ROOT.TGraph() 
    lin.SetName("lin") 
    res=ROOT.TGraph() 
    res.SetName("res") 
    for idx, pt in enumerate(ptbins):
        if idx==len(ptbins)-1: continue
        pt2=ptbins[idx+1]
        m,s=fits[ "res_pt%d_%d"%(pt,pt2)] 
        ptc = (pt+pt2)/2.0
        print "[%.0f,%.0f]: %f %f"%(pt,pt2,m,s)
        lin.SetPoint(lin.GetN(), ptc,ptc*(m+1))
        #lin.SetPoint(lin.GetN(), ptc,m)
        res.SetPoint(res.GetN(), ptc,s/(m+1)) 


    c1=draw_canvas("linearity")
    lin.SetMarkerStyle(20)
    lin.Draw("AP")
    lin.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    #lin.GetYaxis().SetTitle("E(#frac{p_{T}^{raw}-p_{T}^{gen}}{p_{T}^{gen}})")
    lin.GetYaxis().SetTitle("#bar{p}_{T}^{raw} [GeV]")
    lin.GetXaxis().SetTitleOffset(1.2)
    lin.GetYaxis().SetTitleOffset(1.5)
    draw_text()
    c1.Modified()
    c1.Update()

    c2=draw_canvas("resolution")
    res.SetMarkerStyle(20)
    res.Draw("AP")
    res.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    #res.GetYaxis().SetTitle("#sqrt{}V(#frac{p_{T}^{raw}-p_{T}^{gen}}{p_{T}^{gen}})")
    res.GetYaxis().SetTitle("d #bar{p}_{T}/p_{T}")
    res.GetXaxis().SetTitleOffset(1.2)
    res.GetYaxis().SetTitleOffset(1.5)
    draw_text()
    c2.Modified()
    c2.Update()

    raw_input("ok?")
    c0.SaveAs("plot/"+prefix+"fits_"+ftype+".pdf")
    c1.SaveAs("plot/"+prefix+"linearity_"+ftype+".pdf")
    c2.SaveAs("plot/"+prefix+"resolution_"+ftype+".pdf")

if __name__ == "__main__":    
    plot_turnon()
    plot_turnon("pu200")
    plot_turnon_pu()
    plot_resolution()
    plot_resolution("","pu200")
    #plot_resolution("gen")
    #plot_resolution("gen","pu200")
    #plot_resolution("gen","pu140")

