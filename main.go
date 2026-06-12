package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/urfave/cli/v3"
)

var (
	Revision = "Initial Release"
)

func main() {
	cli.VersionPrinter = func(cmd *cli.Command) {
		fmt.Printf("FinTrack version=%s revision=%s", cmd.Root().Version, Revision)
	}

	cmd := &cli.Command{
		Name:    "ftrack",
		Usage:   "ftrack is a tool for managing finnance on the command line.",
		Version: "v1.0.0",
	}

	if err := cmd.Run(context.Background(), os.Args); err != nil {
		log.Fatal(err)
	}

}
