// Leaderboard.h
#pragma once

#include "CoreMinimal.h"
#include "Leaderboard.generated.h"

UCLASS()
class YOURPROJECT_API ALeaderboard {
    GENERATED_BODY()

public:
    ALeaderboard();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Leaderboard")
    TArray<class APlayerScore*> Scores;

    UFUNCTION(BlueprintCallable, Category = "Leaderboard")
    void AddScore(APlayerScore* score);

    UFUNCTION(BlueprintCallable, Category = "Leaderboard")
    void DisplayScores();
}
