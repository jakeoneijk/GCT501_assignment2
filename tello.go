package main

import (
       "fmt"
        "strconv"
        "time"
        "sync/atomic"
        "math"
        "gobot.io/x/gobot"
        "gobot.io/x/gobot/platforms/dji/tello"
      "gobot.io/x/gobot/platforms/leap"
        "gobot.io/x/gobot/platforms/keyboard"
        "encoding/csv"
        "os"
        "log"


)

type pair struct {
        ws float64
        ad float64
        qe float64
        jk float64
        sense float64

}
var PalmPosition []float64
var TelloAD, TelloWS, TelloQE, TelloJK, TelloSense atomic.Value
var valWS, valAD, valQE, valJK int
var valSense float64 
var data = [][]string{{"Line1", "Hello Readers of"}, {"Line2", "golangcode.com"}}

const offset = 100

//const sensitivity = 3

func main() {
        drone := tello.NewDriver("8888")

        keys := keyboard.NewDriver()

        leapMotionAdaptor := leap.NewAdaptor("127.0.0.1:6437")
        l := leap.NewDriver(leapMotionAdaptor)
   
        work := func() {
                TelloAD.Store(float64(0.0))
                TelloWS.Store(float64(0.0))
                TelloQE.Store(float64(0.0))
                TelloJK.Store(float64(0.0))
                TelloSense.Store(float64(0.0))
                valWS = 0
                valAD = 0
                valQE = 0
                valJK = 0
                valSense = 0
                

                keys.On(keyboard.Key, func(data interface{}) {
                        key := data.(keyboard.KeyEvent)

                        if key.Key == keyboard.O {
                                drone.TakeOff()
                        }
                })

                keys.On(keyboard.Key, func(data interface{}) {
                        key := data.(keyboard.KeyEvent)

                        if key.Key == keyboard.P {
                                drone.Land()
                        }
                })


                l.On(leap.HandEvent, func(data interface{}) {
                        //almPosition = data.(leap.Hand).StabilizedPalmPosition
                        PalmPosition = data.(leap.Hand).PalmPosition
                        //fmt.Println(leap.Hand)
                        //TelloQE.Store(data.((leap.Hand).R[0][0]-0.5)*10)//rotate
                        if data.(leap.Hand).S < 1 {
                                TelloWS.Store(float64(0))
                                TelloAD.Store(float64(0))
                                TelloQE.Store(float64(0))
                                TelloJK.Store(float64(0))
                        } else {
                                if PalmPosition[0] < -50{
                                        PalmPosition[0]=-50}
                                if PalmPosition[0] > 50{
                                        PalmPosition[0]=50}
                                PalmPosition[1] = PalmPosition[1]-150
                                if PalmPosition[1] < -50{
                                        PalmPosition[1]=-50}
                                if PalmPosition[1] > 50{
                                        PalmPosition[1]=50}
                                if PalmPosition[2] < -50{
                                        PalmPosition[2]=-50}
                                if PalmPosition[2] > 50{
                                        PalmPosition[2]=50}
                                TelloAD.Store(PalmPosition[0]) //left right/*/10*/
                                TelloJK.Store(PalmPosition[1])//up down/*/12-15*/
                                TelloWS.Store(-(PalmPosition[2]))// forward backward  */8)*/
                                /* rotation qe*/
                        }
                })
                
               

                /* Sensitivity Up*/
                keys.On(keyboard.Key, func(data interface{}) {
                        key := data.(keyboard.KeyEvent)

                        if key.Key == keyboard.ArrowUp {
                                valSense = valSense + 0.2
                                if valSense > 2 {
                                      valSense = 2
                                }
                                TelloSense.Store(float64(valSense))
                        }
                })

                /* Sensitivity Down*/
                keys.On(keyboard.Key, func(data interface{}) {
                        key := data.(keyboard.KeyEvent)

                        if key.Key == keyboard.ArrowDown {
                                valSense = valSense - 0.2
                                if valSense < 0 {
                                        valSense = 0
                                }
                                TelloSense.Store(float64(valSense))
                        }
                })


                // /* CCW */
                // keys.On(keyboard.Key, func(data interface{}) {
                //         key := data.(keyboard.KeyEvent)

                //         if key.Key == keyboard.Q {
                //                 valQE = valQE - 1
                //                 if valQE < -20 {
                //                       valQE = -20
                //                 }
                //                 TelloQE.Store(float64(valQE))
                //         }
                // })

                // /* CW */
                // keys.On(keyboard.Key, func(data interface{}) {
                //         key := data.(keyboard.KeyEvent)

                //         if key.Key == keyboard.E {
                //                 valQE = valQE + 1
                //                 if valQE > 20 {
                //                       valQE = 20
                //                 }
                //                 TelloQE.Store(float64(valQE))
                //         }
                // })
                /*gobot.Every(1*time.second, func() {
                }*/

                gobot.Every(5*time.Millisecond, func() {
                        controlDirection := Direction()

                        switch {
                                case controlDirection.ws > 0:
                                        drone.Forward(tello.ValidatePitch(controlDirection.ws * controlDirection.sense, offset))
                                case controlDirection.ws < 0:
                                        drone.Backward(tello.ValidatePitch(controlDirection.ws * controlDirection.sense, offset))
                                case controlDirection.ws == 0:
                                        drone.Forward(0)
                                        drone.Backward(0)
                                default:
                                        drone.Forward(0)
                                        drone.Backward(0)
                        }

                        switch {
                                case controlDirection.ad > 0:
                                        drone.Right(tello.ValidatePitch(controlDirection.ad * controlDirection.sense, offset))
                                case controlDirection.ad < 0:
                                        drone.Left(tello.ValidatePitch(controlDirection.ad * controlDirection.sense, offset))
                                case controlDirection.ad == 0:
                                        drone.Right(0)
                                        drone.Left(0)
                                default:
                                        drone.Right(0)
                                        drone.Left(0)
                        }

                        switch {
                                case controlDirection.qe > 0:
                                        drone.Clockwise(tello.ValidatePitch(controlDirection.qe * controlDirection.sense, offset))
                                case controlDirection.qe < 0:
                                        drone.CounterClockwise(tello.ValidatePitch(controlDirection.qe * controlDirection.sense, offset))
                                case controlDirection.qe == 0:
                                        drone.Clockwise(0)
                                        drone.CounterClockwise(0)
                                default:
                                        drone.Clockwise(0)
                                        drone.CounterClockwise(0)
                        }

                        switch {
                                case controlDirection.jk > 0:
                                        drone.Up(tello.ValidatePitch(controlDirection.jk * controlDirection.sense, offset))
                                case controlDirection.jk < 0:
                                        drone.Down(tello.ValidatePitch(controlDirection.jk * controlDirection.sense, offset))
                                case controlDirection.jk == 0:
                                        drone.Up(0)
                                        drone.Down(0)
                                default:
                                        drone.Up(0)
                                        drone.Down(0)
                        }
                })
        }

        robot := gobot.NewRobot("tello",
                []gobot.Connection{leapMotionAdaptor},
                []gobot.Device{keys, drone,l},
                work,
        )

       

        robot.Start()
}



func Direction() pair {
        s := pair{ws: 0, ad: 0, qe: 0, jk: 0, sense: 0}
        s.ws = math.Round(TelloWS.Load().(float64))
        s.ad = math.Round(TelloAD.Load().(float64))
        s.qe = math.Round(TelloQE.Load().(float64))
        s.jk = math.Round(TelloJK.Load().(float64))
        s.sense = (TelloSense.Load().(float64))
        if s.ws == 0 && s.ad == 0 && s.jk == 0{
                fmt.Println("손을 펴서 Leap Motion 영역 내에 위치해주세요")
        } else{
                fmt.Println("전후:", s.ws,"좌우:", s.ad, "상하:",s.jk, "(sensitivity:", s.sense, ")")

        }


        rows := [][]string{
		
                {strconv.FormatFloat(s.ws,'f',5,64)},
		{strconv.FormatFloat(s.ad,'f',5,64)},
                {strconv.FormatFloat(s.jk,'f',5,64)},
                {strconv.FormatFloat(s.sense,'f',5,64)},
	}
 
	csvfile, err := os.Create("test.csv")
 
	if err != nil {
		log.Fatalf("failed creating file: %s", err)
	}
 
	csvwriter := csv.NewWriter(csvfile)
 
	for _, row := range rows {
		_ = csvwriter.Write(row)
	}
 
	csvwriter.Flush()
 
	csvfile.Close()

        return s
}