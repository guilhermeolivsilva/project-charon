; ModuleID = 'llvm_type_cast.cpp'
source_filename = "llvm_type_cast.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128"
target triple = "arm64-apple-macosx14.0.0"

@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef i32 @_Z7int_sumii(i32 noundef %0, i32 noundef %1) #0 {
  %3 = alloca i32, align 4
  %4 = alloca i32, align 4
  store i32 %0, ptr %3, align 4
  store i32 %1, ptr %4, align 4
  %5 = load i32, ptr %3, align 4
  %6 = load i32, ptr %4, align 4
  %7 = add nsw i32 %5, %6
  ret i32 %7
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef float @_Z9float_sumff(float noundef %0, float noundef %1) #0 {
  %3 = alloca float, align 4
  %4 = alloca float, align 4
  store float %0, ptr %3, align 4
  store float %1, ptr %4, align 4
  %5 = load float, ptr %3, align 4
  %6 = load float, ptr %4, align 4
  %7 = fadd float %5, %6
  ret float %7
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef signext i8 @_Z8char_sumcc(i8 noundef signext %0, i8 noundef signext %1) #0 {
  %3 = alloca i8, align 1
  %4 = alloca i8, align 1
  store i8 %0, ptr %3, align 1
  store i8 %1, ptr %4, align 1
  %5 = load i8, ptr %3, align 1
  %6 = sext i8 %5 to i32
  %7 = load i8, ptr %4, align 1
  %8 = sext i8 %7 to i32
  %9 = add nsw i32 %6, %8
  %10 = trunc i32 %9 to i8
  ret i8 %10
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define noundef i64 @_Z8long_sumll(i64 noundef %0, i64 noundef %1) #0 {
  %3 = alloca i64, align 8
  %4 = alloca i64, align 8
  store i64 %0, ptr %3, align 8
  store i64 %1, ptr %4, align 8
  %5 = load i64, ptr %3, align 8
  %6 = load i64, ptr %4, align 8
  %7 = add nsw i64 %5, %6
  ret i64 %7
}

; Function Attrs: mustprogress noinline norecurse optnone ssp uwtable(sync)
define noundef i32 @main() #1 {
  %1 = alloca i32, align 4
  %2 = alloca i32, align 4
  %3 = alloca float, align 4
  %4 = alloca i8, align 1
  %5 = alloca i64, align 8
  store i32 0, ptr %1, align 4
  %6 = call noundef i32 @_Z7int_sumii(i32 noundef 23, i32 noundef 13)
  store i32 %6, ptr %2, align 4
  %7 = call noundef float @_Z9float_sumff(float noundef 0x40091EB860000000, float noundef 0x4005AE1480000000)
  store float %7, ptr %3, align 4
  %8 = call noundef signext i8 @_Z8char_sumcc(i8 noundef signext 1, i8 noundef signext 2)
  store i8 %8, ptr %4, align 1
  %9 = call noundef i64 @_Z8long_sumll(i64 noundef 123, i64 noundef 321)
  store i64 %9, ptr %5, align 8
  %10 = load i32, ptr %2, align 4
  %11 = sitofp i32 %10 to float
  %12 = load float, ptr %3, align 4
  %13 = fadd float %11, %12
  %14 = load i8, ptr %4, align 1
  %15 = sext i8 %14 to i32
  %16 = sitofp i32 %15 to float
  %17 = fadd float %13, %16
  %18 = load i64, ptr %5, align 8
  %19 = sitofp i64 %18 to float
  %20 = fadd float %17, %19
  %21 = fptosi float %20 to i32
  %22 = call i32 (ptr, ...) @printf(ptr noundef @.str, i32 noundef %21)
  ret i32 0
}

declare i32 @printf(ptr noundef, ...) #2

attributes #0 = { mustprogress noinline nounwind optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #1 = { mustprogress noinline norecurse optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #2 = { "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 1}
!3 = !{i32 7, !"frame-pointer", i32 1}
!4 = !{!"Homebrew clang version 17.0.3"}
