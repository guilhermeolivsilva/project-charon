; ModuleID = 'llvm_structs_and_arrays.cpp'
source_filename = "llvm_structs_and_arrays.cpp"
target datalayout = "e-m:o-i64:64-i128:128-n32:64-S128"
target triple = "arm64-apple-macosx14.0.0"

%struct.my_type = type { i32, ptr, float, i32, i64 }
%struct.my_type_clone = type { i32, ptr, float, i32, i64 }
%struct.another_type = type { i32, i32, i32 }

@some_integer = global i32 0, align 4
@some_array = global [5 x i32] zeroinitializer, align 4

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define void @_Z4testv(ptr noalias sret(%struct.my_type) align 8 %0) #0 {
  ret void
}

; Function Attrs: mustprogress noinline nounwind optnone ssp uwtable(sync)
define void @_Z10test_clonev(ptr noalias sret(%struct.my_type_clone) align 8 %0) #0 {
  ret void
}

; Function Attrs: mustprogress noinline norecurse optnone ssp uwtable(sync)
define noundef i32 @main() #1 {
  %1 = alloca %struct.my_type, align 8
  %2 = alloca [5 x %struct.another_type], align 4
  %3 = getelementptr inbounds %struct.my_type, ptr %1, i32 0, i32 0
  store i32 1, ptr %3, align 8
  %4 = call noalias noundef nonnull ptr @_Znam(i64 noundef 16) #3
  %5 = getelementptr inbounds %struct.my_type, ptr %1, i32 0, i32 1
  store ptr %4, ptr %5, align 8
  %6 = getelementptr inbounds %struct.my_type, ptr %1, i32 0, i32 2
  store float 1.000000e+00, ptr %6, align 8
  %7 = getelementptr inbounds %struct.my_type, ptr %1, i32 0, i32 3
  store i32 4, ptr %7, align 4
  %8 = getelementptr inbounds %struct.my_type, ptr %1, i32 0, i32 4
  store i64 321, ptr %8, align 8
  %9 = getelementptr inbounds [5 x %struct.another_type], ptr %2, i64 0, i64 0
  %10 = getelementptr inbounds %struct.another_type, ptr %9, i32 0, i32 0
  store i32 1, ptr %10, align 4
  ret i32 0
}

; Function Attrs: nobuiltin allocsize(0)
declare noundef nonnull ptr @_Znam(i64 noundef) #2

attributes #0 = { mustprogress noinline nounwind optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #1 = { mustprogress noinline norecurse optnone ssp uwtable(sync) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #2 = { nobuiltin allocsize(0) "frame-pointer"="non-leaf" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="apple-m1" "target-features"="+aes,+crc,+dotprod,+fp-armv8,+fp16fml,+fullfp16,+lse,+neon,+ras,+rcpc,+rdm,+sha2,+sha3,+v8.1a,+v8.2a,+v8.3a,+v8.4a,+v8.5a,+v8a,+zcm,+zcz" }
attributes #3 = { builtin allocsize(0) }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 8, !"PIC Level", i32 2}
!2 = !{i32 7, !"uwtable", i32 1}
!3 = !{i32 7, !"frame-pointer", i32 1}
!4 = !{!"Homebrew clang version 17.0.3"}
